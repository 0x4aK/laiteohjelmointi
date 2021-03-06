icons = {
    'humidity': ((0, 0, 1, 0, 0, 0),
                 (0, 1, 1, 1, 0, 0),
                 (1, 1, 1, 1, 1, 0),
                 (1, 1, 1, 1, 1, 0),
                 (0, 1, 1, 1, 0, 0)),

    'pressure': ((0, 1, 0, 0, 0, 1),
                 (0, 1, 0, 0, 1, 1),
                 (0, 1, 0, 0, 0, 1),
                 (1, 1, 1, 0, 1, 1),
                 (0, 1, 0, 0, 0, 1)),

    'temp': ((0, 1, 0, 0, 1, 1),
             (0, 0, 0, 1, 0, 0),
             (0, 0, 0, 1, 0, 0),
             (0, 0, 0, 1, 0, 0),
             (0, 0, 0, 0, 1, 1)),

    'ip': ((0, 0, 1, 0, 0, 0),
           (0, 0, 1, 0, 0, 0),
           (1, 1, 1, 1, 1, 0),
           (1, 0, 1, 0, 1, 0),
           (1, 0, 1, 0, 1, 0)),
}

if __name__ == "__main__":
    for value in icons.values():
        for line in value:
            print("".join('■' if x else ' ' for x in line))

        print("")
