import errors
import configuration as cfg
import genea


def main():
    config = cfg.load_config("config.ini")

    cmd = ""
    while cmd != "end":

        msg = input("> ")
        args = msg.split(" ")

        if len(args) == 0:
            continue

        cmd = args[0]

        if cmd == "run":
            genea.start(config)
        '''
        if cmd == "graph":
            if len(args) < 2:
                print("Oops!", "You have to enter which solution you want to plot.")
                continue
            print(genea.show_graph(args[1], config))
        '''
        if len(args) < 2:
            continue

        if cmd == "config":
            try:
                config = cfg.load_config(args[1])
            except errors.InvalidConfigError:
                print("Oops!", "Invalid configuration file. Please provide correct path.")
                continue
            print(f"Success! Loaded configuration file from:\n\t {args[1]}")

        if cmd == "path":
            if len(args) < 2:
                continue
            config.file_path = args[1]
            print(f"Success! Set output file path to:\n\t {args[1]}")


if __name__ == "__main__":
    main()
