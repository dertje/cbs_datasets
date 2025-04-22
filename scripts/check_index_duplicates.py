from fetch import get_datasets_names
from typing import List


def write_to_txt_file(content: List[str], file_name: str) -> None:
    """Takes a list of strings and writes all the items with a newline character to a given txt file.

    Args:
        content (List[str]): A list of string items.
        file_name (_type_): The file to write the list items to.
    """
    with open(file_name, "w") as file:
        for dataset_name in content:
            file.write(dataset_name+"\n")
	
def check_differences(list1: List[str], list2: List[str]) -> List[str] | List[str] | list[str]:
    """Takes 2 lists and checks which items are in both lists.

    Args:
        list1 (List[str]): A list with string items.
        list2 (List[str]): Another list with string items.

    Returns:
        List[str]: A list with items that appear in both the orignal lists.
        List[str]: A list with items that only appear in list1.
        list[str]: A list with items that only appear in list2.
    """
    in_both_lists = []
    only_in_list1 = []
    list1_copy = list1[:]

    for ele in list1_copy:
        if ele in list2:
            in_both_lists.append(ele)
            list1.remove(ele)
            list2.remove(ele)
        else:
            only_in_list1.append(ele)

    return in_both_lists, list1, list2

def main():
    opendata_index = get_datasets_names("https://opendata.cbs.nl/odatafeed")
    dataderden_index = get_datasets_names("https://dataderden.cbs.nl/odatafeed")
    write_to_txt_file(opendata_index, "../output_files/indexes_check/opendata_index.txt")
    write_to_txt_file(dataderden_index, "../output_files/indexes_check/dataderden_index.txt")

    all_dataderden_in_opendata = all(item in opendata_index for item in dataderden_index)
    all_opendata_in_dataderden = all(item in dataderden_index for item in opendata_index)
    print(f"All datasets from dataderden index are in the opendata index: {all_dataderden_in_opendata}")
    print(f"All datasets from opendata index are in the dataderden index: {all_opendata_in_dataderden}")
    if all_dataderden_in_opendata and all_opendata_in_dataderden:
        print(f"The lists are equal.")
    else:
        print("The lists are not equal, see output txt files.")
        in_both_lists, only_in_dataderden, only_in_opendata = check_differences(dataderden_index, opendata_index)
        write_to_txt_file(in_both_lists, "../output_files/indexes_check/in_both_lists.txt")
        write_to_txt_file(only_in_dataderden, "../output_files/indexes_check/only_in_dataderden.txt")
        write_to_txt_file(only_in_opendata, "../output_files/indexes_check/only_in_opendata.txt")


if __name__=='__main__':
    main()