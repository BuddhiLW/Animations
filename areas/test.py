test = "abc"
match test:
    case "abc":
        print("Matched abc")
    case "def":
        print("Matched def")
    case _:
        print("Didn't match")
