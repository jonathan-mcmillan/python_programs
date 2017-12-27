def yesOrNo(prompt):
    while True:
        ans = raw_input(promt)
        if ans == 'yes':
            return True
        if ans == 'no':
            return False
        print 'must be "yes" or "no"'
