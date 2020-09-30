import json

def getcityinformation(city):

    results = []

    # Opening of the json file about cities and their information
    with open('city.list.json') as json_file:
        data = json.load(json_file)
        for d in data:
            if d['name'].lower() == city.lower():
                results.append(d)
    json_file.close()
    if len(results) == 0:
        print(city, 'not found')
        quit()

    elif len(results) == 1:
        return results
# If the search yields more than one result, this branch activates and as a result gives just one unambiguous result
    else:
        print('Which one? ')
        for r in results:
            if len(r['state']) != 0:
                print('({}, {})'.format(r['state'], r['country']))
            else:
                print(r['country'])
        choice = input()
        yield_result = []
        for r in results:
            if choice.upper() == r['state'] or choice.upper() == r['country']:
                yield_result.append(r)

        if len(yield_result) == 1:
            return yield_result
        else:
            print('Please choose only one of these options with a number: ')
            for i in yield_result:
                if len(i['state']) != 0:
                    print('({}, {})'.format(i['state'], i['country']))
                else:
                    print('(country - {})'.format(i['country']))
            choice_index = input()
            final_city = (yield_result[int(choice_index) - 1])
            if len(final_city) == 5:
                return final_city

