from arvancli.common.cloud_provider import CloudProviderBuilder
from arvancli.common.utils import Session
import sys
import os
from argparse import ArgumentParser
from configparser import ConfigParser

class Shell:
    def __init__(self, argv: list) -> None:
        self._argv = argv
        self._build_parser()
        self._config_path = f'{os.path.expanduser("~")}/.arvancli.ini'
        self._argv_position = 0
    def main(self) -> None:
       builder = CloudProviderBuilder(self._subparsers)
       #TODO: make argparse parse subcommands partialy.
       if self._check_and_set_command():
           self._cloud_provider = builder()
           self._cloud_service  = self._cloud_provider.get(self._current_command)
           if self._check_and_set_command():
                self._cloud_entity   = self._cloud_service.get(self._current_command)
                parsed_args = self._parse_args()
                self._conf_manager({}, 'general')
                session = Session(eval(self._token), eval(self._zone))
                if self._check_and_set_command():
                    self._cloud_entity.run(self._current_command, session, parsed_args)
       else:
           parsed_args = self._parse_args()
           self._conf_manager(parsed_args, 'general')
    def _check_and_set_command(self) -> bool:
        shell_commands = [{'configure', '--help'}, {'--help'}, {'--help'}]
        if self._argv[self._argv_position] not in shell_commands[self._argv_position]:
            self._current_command = self._argv[self._argv_position] 
            result = True
        else:
            result = False
        self._argv_position += 1
        return result
    def _build_parser(self) -> None:
        self._parser = ArgumentParser(description='Arvan CLI')
        self._subparsers = self._parser.add_subparsers()
        self.config_subparser = self._subparsers.add_parser('configure')
        self.config_subparser.add_argument('--token', help='')
        self.config_subparser.add_argument('--zone', help='')
    def _parse_args(self) -> dict:
        return vars(self._parser.parse_known_args()[0])
    def _conf_manager(self, parsed_args: dict, section: str) -> None:
        config_object = ConfigParser()
        if parsed_args:
            self._update_config(config_object, parsed_args, section)
            sys.exit()
        else:
            self._read_config(config_object, section)
    def _read_config(self, config_object: ConfigParser, section: str) -> None:
        config_object.read(self._config_path)
        if section not in config_object:
            config_object[section] = {}
        else:
            for conf in config_object[section]:
                exec(f'self._{conf} = config_object["{section}"]["{conf}"]')
    def _update_config(self, config_object: ConfigParser, parsed_args: dict, section: str) -> None:
        self._read_config(config_object, section)
        for arg in parsed_args:
            if parsed_args[arg] is not None:
                config_object[section][arg] = f'"{parsed_args[arg]}"' 
        with open(self._config_path, 'w+') as conf:
            config_object.write(conf)
    
def main(argv=None):
     
    return Shell(sys.argv[1:]).main()

if __name__ == "__main__":
    sys.exit(main())
