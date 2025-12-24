import json, time, sys, threading
from pathlib import Path
from rich.console import Console
from rich.panel import Panel

from core.utils import load_config, ensure_data_files, log_event
from core.memory import Memory
from core.gpt_interface import GPTClient
from core.scheduler import Scheduler
from core.voice import VoiceAssistant
from plugins import registry as plugin_registry

console = Console()

def banner():
    console.print(Panel.fit("[bold cyan]Jarvis-AI[/] — ready to assist ✨", border_style="cyan"))

def main():
    cfg = load_config()
    ensure_data_files()
    memory = Memory(Path("data/memory.json"))
    gpt = GPTClient(cfg)
    sched = Scheduler()
    voice = VoiceAssistant(cfg)

    # register sample recurring job
    sched.add_recurring_job("heartbeat", "interval", hours=1, func=lambda: log_event("Heartbeat tick"))

    banner()
    console.print("[dim]Type 'help' for commands. Say wake word to use voice. Ctrl+C to exit.[/dim]")

    while True:
        try:
            cmd = input("\n> ").strip()
            if not cmd:
                continue
            if cmd.lower() in ("quit", "exit"):
                break
            if cmd.lower() == "help":
                console.print("""
Commands:
  ask <prompt>        → Ask GPT
  remember <note>     → Save a memory
  recall              → Show last 5 memories
  schedule <text>     → Schedule a reminder (e.g., 'in 10 minutes drink water')
  run <plugin> <arg>  → Run a plugin (weather <city>, news <topic>)
  voice on/off        → Enable or disable mic listener
  gui                 → How to start GUI
  config              → Print loaded config keys
""")
                continue
            if cmd.startswith("ask "):
                prompt = cmd[4:].strip()
                reply = gpt.chat(prompt, memory=memory)
                console.print(Panel(reply, title="GPT", border_style="magenta"))
                continue
            if cmd.startswith("remember "):
                note = cmd[len("remember "):].strip()
                memory.add(note)
                console.print("[green]Saved to memory.[/green]")
                continue
            if cmd == "recall":
                for i, m in enumerate(memory.recent(5), 1):
                    console.print(f"{i}. {m['text']} [dim]({m['ts']})[/]")
                continue
            if cmd.startswith("schedule "):
                text = cmd[len("schedule "):].strip()
                when = sched.parse_and_schedule(text)
                console.print(f"[green]Scheduled:[/green] {text} → [bold]{when}[/]")
                continue
            if cmd.startswith("run "):
                parts = cmd.split(maxsplit=2)
                if len(parts) < 2:
                    console.print("[red]Usage: run <plugin> [args][/red]")
                    continue
                plugin = parts[1]
                arg = parts[2] if len(parts) == 3 else ""
                func = plugin_registry.get(plugin)
                if not func:
                    console.print(f"[red]Unknown plugin:[/red] {plugin}. Try: {', '.join(plugin_registry.keys())}")
                    continue
                try:
                    out = func(arg, cfg)
                    console.print(Panel(out, title=f"Plugin: {plugin}", border_style="blue"))
                except Exception as e:
                    console.print(f"[red]Plugin error:[/red] {e}")
                continue
            if cmd == "voice on":
                voice.start_background_listener(gpt, memory)
                console.print("[green]Voice listener ON.[/green]")
                continue
            if cmd == "voice off":
                voice.stop_background_listener()
                console.print("[yellow]Voice listener OFF.[/yellow]")
                continue
            if cmd == "gui":
                console.print("Open a new terminal, then: cd gui && npm install && npm start")
                continue
            if cmd == "config":
                console.print(json.dumps({k: ('***' if 'KEY' in k or 'SECRET' in k else v) for k,v in cfg.items()}, indent=2))
                continue

            console.print("[yellow]Unknown command. Type 'help'.[/yellow]")
        except KeyboardInterrupt:
            break
        except Exception as e:
            console.print(f"[red]Error:[/red] {e}")

    console.print("[dim]Shutting down...[/dim]")

if __name__ == "__main__":
    main()
