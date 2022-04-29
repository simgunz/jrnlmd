import click


class AliasedGroup(click.Group):
    def get_command(self, ctx, cmd_name):
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv
        else:
            ctx.ensure_object(dict)
            ctx.obj["PRE-TEXT"] = cmd_name
            return click.Group.get_command(self, ctx, "add")
