import unicodedata
import itertools
import re

from irc3.plugins.command import command
import irc3

@irc3.plugin
class Plugin:
    def __init__(self, bot):
        self.bot = bot
        with open('sl.txt') as f:
            self.sl = f.read().split('\n')
        # https://modern.ircdocs.horse/formatting.html
        self.color_re = re.compile('\x03(\d\d?(,\d\d?)?)?|\x04([0-9a-f]{6}(,[0-9a-f]{6})?)?', re.ASCII)

    @command(permission='view')
    def meinnetz(self, mask, target, args):
        """Eigenes Netz festlegen

            %%meinnetz [<netz>...]
        """
        print('{mask} meinnetz {args}'.format(mask=mask, args=args))
        netz = args['<netz>'] or None
        if netz is not None:
            netz = ' '.join(netz)
        self.bot.db.set(mask.nick, netz=netz)
        yield 'ack'

    @command(permission='view')
    def netz(self, mask, target, args):
        """Netz abfragen

            %%netz [<nick>]
        """
        print('{mask} netz {args}'.format(mask=mask, args=args))
        nick = args['<nick>']
        if nick is None:
            nick = mask.nick
        yield self.bot.db.get(nick, {}).get('netz', None) or 'Nichts bekannt über {nick}'.format(nick=nick)

    @command(permission='admin', show_in_help_list=False)
    def netzoverride(self, mask, target, args):
        """Netz überschreiben

            %%netzoverride <nick> [<netz>...]
        """
        print('{mask} netzoverride {args}'.format(mask=mask, args=args))
        netz = args['<netz>'] or None
        if netz is not None:
            netz = ' '.join(netz)
        self.bot.db.set(args['<nick>'], netz=netz)
        yield 'ack'

    @command(permission='view')
    def netzinfo(self, mask, target, args):
        """Netzbot Infos

            %%netzinfo
        """
        print('{mask} netzinfo {args}'.format(mask=mask, args=args))
        yield 'Nutzer können mit !meinnetz [<Netz>...] ihr Netz festlegen. Mit !netz [<Nick>] kann es abgefragt werden. !allenetze zeigt die Anzahl der registrierten Nutzer in jedem Netz.'

    def clean_netz(self, netz):
        """Remove colors and control characters"""
        netz = self.color_re.sub('', netz)
        return ''.join([c for c in netz if unicodedata.category(c) != 'Cc'])

    @command(permission='view')
    def allenetze(self, mask, target, args):
        """Zeigt alle eingetragenen Netze an

            %%allenetze
        """
        print('{mask} allenetze {args}'.format(mask=mask, args=args))
        # uncool hack (.backend.db), as there is no official way to enumerate first level keys
        netze = [self.clean_netz(obj['netz']) for obj in self.bot.db.backend.db.values() if obj.get('netz', None) is not None]
        sizemap = {}
        for key, group in itertools.groupby(netze):
            # unsorted, so will get multiple calls for one key
            s = sizemap.get(key, 0)
            sizemap[key] = s + len(list(group))
        # sort by number (bigger first) and name (case insensitive)
        output = sorted(sizemap.items(), key=lambda t: (-t[1], t[0].lower()))
        yield ', '.join(['{0[0]}: {0[1]}'.format(t) for t in output])

    @command(permission='view')
    def sl(self, mask, target, args):
        """list directory contents

            %%sl [<options>...]
        """
        print('{mask} sl {args}'.format(mask=mask, args=args))
        yield 'CHOO CHOO!'
        for line in self.sl:
            self.bot.privmsg(mask.nick, line)

    @command(permission='view', show_in_help_list=False)
    def syn(self, mask, target, args):
        """syn

            %%syn [<ignore>...]
        """
        print('{mask} syn {args}'.format(mask=mask, args=args))
        yield 'don\'t be silly now...'

