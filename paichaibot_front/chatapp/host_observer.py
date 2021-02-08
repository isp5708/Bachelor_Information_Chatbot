
class Singleton:
    __instance = None

    @classmethod
    def __getInstance(cls):
        return cls.__instance
    
    @classmethod
    def instance(cls, *arg, **kargs):
        cls.__instance = cls(*arg, **kargs)
        cls.instance = cls.__getInstance
        return cls.__instance


class HostObserver(Singleton):
    def __init__(self):
        self.hosts = []
    
    def add(self, host):
        if host not in self.hosts:
            self.hosts.append(host)
            print(host + '사용자 접속!')
            return True
        else:
            print('동일 사용자 이름 접속!')
            return False
    
    def remove(self, host):
        try:
            self.hosts.remove(host)
            print(host + '사용자 연결 해제')
            return True
        except:
            print('없는 사용자를 지우려고 함')
            return False
        
    def notify(self):
        [o.notify(self) for o in self.hosts]