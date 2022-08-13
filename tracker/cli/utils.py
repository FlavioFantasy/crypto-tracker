import sys
from typing import List

import click


def template_to_title(template) -> str:
    column_names = [s.split(":")[0] for s in template.strip("{}").split("}{")]
    column_dict = {t: t for t in column_names}
    return template.format(**column_dict)


def echo_success(msg: str, nl: bool = True) -> None:
    click.echo(click.style(msg, fg="green"), nl=nl)


def echo_warning(msg: str, nl: bool = True) -> None:
    click.echo(click.style(msg, fg="yellow"), nl=nl)


def echo_fail(msg: str, nl: bool = True) -> None:
    click.echo(click.style(msg, fg="red"), nl=nl)


def exit_with_failure(msg: str, nl: bool = True) -> None:
    echo_fail(msg, nl=nl)
    sys.exit(1)


# region help cmd
_HELP_CMD = "help"


class TrackerClickGroup(click.Group):
    """Adds a custom help command that shows the whole commands subtree
    The additional command is the last one when listing commands
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.list_commands = self.list_commands_for_help
        self.add_command(help, name=_HELP_CMD)

    def list_commands_for_help(self, ctx):
        """reorder the list of commands when listing the help"""
        commands = super(TrackerClickGroup, self).list_commands(ctx)
        commands.remove(_HELP_CMD)
        commands.append(_HELP_CMD)
        return commands


@click.command()
@click.pass_context
def help(ctx) -> None:
    """Describe usage and list subcommands recursively"""
    cmd_ctx = ctx.parent
    ctx_dict = cmd_ctx.to_info_dict()["command"]

    usage = cmd_ctx.get_usage()
    res = [usage, ""]
    if descr := ctx_dict["help"]:
        res.extend([" " * 4 + descr.strip(" "), ""])
    res.append("Subcommands:")
    res.extend(recurse_subcmds(ctx_dict))
    usage = click.style(
        f"{usage.split(' ')[1]} [cmd [subcmd ...]] {_HELP_CMD}", italic=True, bold=True
    )
    res.extend(["", f"use '{usage}' to get this message", ""])
    click.echo("\n".join(res))


def recurse_subcmds(dict_ctx, indent="") -> List[str]:
    """Explore the comands subtree to produce a list of indented command description strings"""
    if "commands" not in dict_ctx:
        return []
    indent += "  "
    res = []
    for cmd_name, child_ctx in sorted(dict_ctx["commands"].items()):
        if cmd_name == _HELP_CMD:
            continue
        cmd_str = indent + "- " + click.style(cmd_name, bold=True)
        # take different docstring formats into account
        descr = child_ctx["short_help"] or child_ctx["help"] or ""
        descr = descr.split("\n")[0].strip(" ")

        res.append(f"{cmd_str.ljust(40)} {descr}")
        res.extend(recurse_subcmds(child_ctx, indent))
    return res


# endregion
