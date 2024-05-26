from controller import BrightnessController
from rich import print

import msvcrt

class Interface():
    def __init__(self, controller: BrightnessController) -> None:
        self.controller = controller

    def start(self) -> None: 
        """Starting a program and requesting a command"""

        self._print_menu()
        try:
            command = int(input('Enter a command: '))
            self.execute_command(command)
        except ValueError:
            print('\n[bold red]You entered the command incorrectly or there is no such command![/bold red]')
            self._press_to_continue()
            self.start()

    def execute_command(self, command: int) -> None:
        """Executes the given command"""
        
        commands = {
            1: self.brightness_command,
            2: self.set_mode,
            3: self.create_mode,
            4: self.delete_mode,
            5: self.get_mode_list,
            6: exit,
        }

        action = commands.get(command)

        if action:
            action()
        else:
            print('\n[bold red]There is no such command[/bold red]')
            self._press_to_continue()
        
        self.start()

    def brightness_command(self) -> None:
        """The command asks which monitor and what brightness to change it to"""
        monitor_list = self.controller.get_monitors()
        try:
            #I made minus 1 because the user will choose first or second monitor, but not zero monitor
            monitor = (int(input(f'\nYou have {len(monitor_list)} monitors ({monitor_list}), write which one you need (in numbers): ')) - 1)
            if monitor < 0:
                raise IndexError
            
            percentage = int(input(f'Set a new brightness for your monitor to range from 1 to 100  (brightness now - {self.controller.get_brightness(monitor)}): '))
            self.controller.set_brightness(percentage, monitor)
            
            return
        
        except ValueError:
            print('\n[bold red]Enter the number correctly![/bold red]')
        except IndexError:
            print('\n[bold red]You have selected a non-existent monitor!(counting starts from one)[/bold red]')
        except Exception as e:
            print('[bold red]an unexpected error occured: {e}[/bold red]')
        
        self._press_to_continue()
    
    def set_mode(self):
        """Asks ans sets the selected brightness mode"""
        print('[i]You can always add some new modes[/i]')
        
        modes = list(self.controller.ModeManager.get_all_modes())
        for i, mode_name in enumerate(modes, start=1):
            print(f'#{i}. {mode_name}')

        try:
            selected_mode = (int(input('Which one do you want to set: ')) - 1)
            if selected_mode < 0:
                raise IndexError
            
            self.controller.set_mode(selected_mode)
            
            return
        
        except ValueError:
            print('\n[bold red]Enter the mode correctly![/bold red]')
        except IndexError:
            print('\n[bold red]There is no such mode[/bold red]')
        except Exception as e:
            if 'Incompatible number of monitors' in str(e):
                print('\n[bold red]You have selected a mode with an incompatible number of monitors[/bold red]')
            else:
                print(f'[bold red]an unexpected error occured: {e}[/bold red]')

        self._press_to_continue()
   
    def create_mode(self) -> None:
        name = input('Enter the name of the new mode: ')

        brightness = [] 
        try:
            for i in range(1, len(self.controller.get_monitors())+1):
                new_bright = int(input(f'Enter the brightness you need for {i} monitor( {self.controller.get_monitors()[i-1]} ): '))
                if new_bright not in range(0, 101):
                    raise IndexError
                
                brightness.append(new_bright)

            self.controller.create_new_mode(name, brightness)
            print('\n[bold green]Done![/bold green]')

            return
        
        except ValueError:
            print('\n[bold red]Enter the number correctly![/bold red]')
        except IndexError:
            print('\n[bold red]Enter a number in the range from 0 to 100![/bold red]')
        except Exception as e:
            print(f'[bold red]an unexpected error occured: {e}[/bold red]')

        self._press_to_continue()

    def delete_mode(self) -> None:
        print(f'Mode names: {list(self.controller.ModeManager.get_all_modes())}')
        name = input('Enter the name you want to delete: ')
        try:
            self.controller.ModeManager.delete_mode(name)
        except KeyError:
            print('\n[bold red]There is no such mode![/bold red]')
            self._press_to_continue()
        else:
            print('\n[bold green]Done![/bold green]')

    def get_mode_list(self) -> None:
        data = self.controller.ModeManager.get_all_modes()
        
        print() # makes empty space in the console
        for mode_name in data.keys():
            print(f'[bold blue]Name:[/bold blue] {mode_name} | brightness for {len(data[mode_name])} monitors: {data[mode_name]}')

        self._press_to_continue()

    def _print_menu(self):
        menu_text = ('\n[bold]This program for setting and controlling the brightness of monitors/displays[/bold]\n'
              '[i](write the number of the command you want to execute)[/i]\n'
              '\n[——————————————— [bold blue]Command List[/bold blue] ———————————————]\n'
              '\n[bold red]#[/bold red] 1. Set the desired brightness\n'
              '\n[bold red]#[/bold red] 2. Select the desired brightness mode\n'
              '\n[bold red]#[/bold red] 3. Create a new mode\n'
              '\n[bold red]#[/bold red] 4. Deletes an existing mode\n'
              '\n[bold red]#[/bold red] 5. Gives a list of all modes that exist\n'
              '\n[bold red]#[/bold red] 6. Exit the program\n'
              )
        
        print(menu_text)

    def _press_to_continue(self) -> None:
        print("\nPress any key to continue...")
        msvcrt.getch()

if __name__ == '__main__':
    controller = BrightnessController()
    interface = Interface(controller)
    interface.start() 