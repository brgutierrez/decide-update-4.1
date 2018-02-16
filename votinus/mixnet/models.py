import requests

from django.db import models

from .mixcrypt import MixCrypt


# number of bits for the key, all auths should use the same number of bits
# TODO: move this to the settings
B = 8


class Auth(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField()
    me = models.BooleanField(default=False)

    def __str__(self):
        return self.url


class Key(models.Model):
    p = models.IntegerField()
    g = models.IntegerField()
    y = models.IntegerField()
    x = models.IntegerField(blank=True, null=True)

    def __str__(self):
        if self.x:
            return "{},{},{},{}".format(self.p, self.g, self.y, self.x)
        else:
            return "{},{},{}".format(self.p, self.g, self.y)


class Mixnet(models.Model):
    vote_id = models.PositiveIntegerField()
    auths = models.ManyToManyField(Auth, related_name="mixnets")
    key = models.ForeignKey(Key, blank=True, null=True,
                            related_name="mixnets",
                            on_delete=models.SET_NULL)
    pubkey = models.ForeignKey(Key, blank=True, null=True,
                               related_name="mixnets_pub",
                               on_delete=models.SET_NULL)

    def __str__(self):
        auths = ", ".join(a.name for a in self.auths.all())
        return "Vote: {}, Auths: {}\nPubKey: {}".format(self.vote_id,
                                                        auths, self.pubkey)

    def gen_key(self, p=0, g=0):
        crypt = MixCrypt(bits=B)
        if self.key:
            k = crypt.setk(self.key.p, self.key.g, self.key.y, self.key.x)
        elif (not g or not p):
            k = crypt.genk()
            key = Key(p=k.p, g=k.g, y=k.y, x=k.x)
            key.save()

            self.key = key
            self.save()
        else:
            k = crypt.getk(p, g)
            key = Key(p=k.p, g=k.g, y=k.y, x=k.x)
            key.save()

            self.key = key
            self.save()

    def chain_call(self, path, data):
        from .serializers import AuthSerializer

        next_auths = self.auths.filter(me=False)
        data.update({
            "auths": AuthSerializer(next_auths, many=True).data,
            "vote": self.vote_id,
        })

        if next_auths:
            url = "{}/{}/".format(next_auths[0].url, path)
            resp = requests.post(url, json=data)
            resp.json()
            return resp.json()

        return None