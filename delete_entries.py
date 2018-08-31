def delete_false_positive(mylist):
    new_list = []
    delete = False
    for ev in mylist:

        if 'Start ' in ev.description:
            delete = False

        if not delete:
            new_list.append(ev)

        if 'End ' in ev.description:
            delete = True

    return new_list
