def debug(f):
    def new_function(a, b):
        print("Function add() called!")
        return f(a, b)
    return new_function
@debug
def add(a, b):
    return a + b
print(add(7, 5))
def cantidad(arr,ent):
	return arr.count(ent)
print(cantidad([2,4,5,6,7,3,2,2],2))