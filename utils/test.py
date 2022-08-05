
# print the list 5 by 5
def print_list(lst: list) -> None:
    for i in range(0, len(lst), 5):
        print(lst[i:i+5])
    print()
    return None

# test above
if __name__ == '__main__':
    print_list([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])