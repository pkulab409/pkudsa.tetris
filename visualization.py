def visual(lis):
    c=reverse(lis)
    for i in lis:
        for j in i:
            if j==0:
                print("0",end="")
            else:
                print("@",end="")
        print("")