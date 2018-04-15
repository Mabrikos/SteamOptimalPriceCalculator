while True:
    try:
        exec(open('SOPC.py').read())
    except Exception as e:
        print ("Exception occured: ", e)
