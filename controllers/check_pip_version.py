try:
    import pip
    print (pip.__version__)
except:
    print ("No pip found")    
    exit(2)

exit(0)