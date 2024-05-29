class MyClass:
    def my_method(self, param1, param2=10, param3="default"):
        print("param1:", param1)
        print("param2:", param2)
        print("param3:", param3)

# Criar uma instância da classe
obj = MyClass()

# Chamada do método com todos os parâmetros
obj.my_method(450)

# Chamada do método com dois parâmetros
obj.my_method(5, 20)

# Chamada do método com todos os parâmetros especificados
obj.my_method(5, 20, "custom")
