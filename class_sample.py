class Shop:
    def __init__(self, name, shop_type, address):
        self.name = name
        self._shop_type = shop_type
        self.address = address
    @property
    def shop_type(self):
        return self._shop_type

    @shop_type.setter
    def shop_type(self, shop_type):
        self._shop_type = shop_type

    def show_info(self):
        print("상점정보 (%s)\n\
        유형: %s\n\
        주소: %s" % (self.name, self.shop_type, self.address))

    @staticmethod
    def make_dummy_shop():
        '''
        name: untitled
        shop_type: untitled
        address: unknown
        의 속성을 갖는 Shop 객체를 생성해 리턴
        '''
        return Shop("untitled", "untitled", "unknown"   )

    def change_type(self, new_shop_type):
        self.shop_type = new_shop_type

class Restaurant(Shop):
    def show_info(self):
        print("식당 (%s)\n\
        유형: %s\n\
        주소: %s" % (self.name, self.shop_type, self.address))

'''
Shop클래스에 change_type인스턴스 메서드를 추가하고, 상점유형(shop_type)을 변경할 수 있는 기능을 추가한다

새로운 Shop인스턴스를 하나 생성하고,
show_info() 인스턴스 메서드를 사용해 본 후
change_type메서드를 사용해 shop_type을 변경시키고
다시 show_info()메서드를 실행해 결과가 잘 반영되었는지 확인한다

'''
