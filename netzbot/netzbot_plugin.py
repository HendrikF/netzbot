from irc3.plugins.command import command
import irc3


@irc3.plugin
class Plugin:

    def __init__(self, bot):
        self.bot = bot

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
        yield 'ok'

    @command(permission='view')
    def netz(self, mask, target, args):
        """Netz abfragen

            %%netz [<nick>]
        """
        print('{mask} netz {args}'.format(mask=mask, args=args))
        nick = args.get('<nick>', mask.nick)
        yield self.bot.db.get(nick, {}).get('netz', None) or 'Nichts bekannt über {nick}'.format(nick=nick)

    @command(permission='admin')
    def netzoverride(self, mask, target, args):
        """Netz überschreiben

            %%netzoverride <nick> [<netz>...]
        """
        print('{mask} netzoverride {args}'.format(mask=mask, args=args))
        netz = args['<netz>'] or None
        if netz is not None:
            netz = ' '.join(netz)
        self.bot.db.set(args['<nick>'], netz=netz)
        yield 'ok'

    @command(permission='view')
    def netzinfo(self, mask, target, args):
        """Netzbot Infos

            %%netzinfo
        """
        print('{mask} netzinfo {args}'.format(mask=mask, args=args))
        yield 'Nutzer können mit !meinnetz [<Netz>...] ihr Netz festlegen. Mit !netz [<Nick>] kann es abgefragt werden. Admin ist h3ndr1k.'

