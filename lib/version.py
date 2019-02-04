from colored import fg, bg, attr

class VersionInfo:

    def __init__(self, v):
        self.rs = attr('reset')
        self.top = fg(4)+"        ╔═══════════════╗"+self.rs
        self.mid = fg(4)+"        ║"+self.rs+" - "+fg(8)+"Scanomaly"+self.rs
        self.mid += " - "+fg(4)+"║"+self.rs
        self.bottom = fg(4)+"        ╚═══════════════╝"+self.rs
        self.info = fg(8)+"Automated web fuzzing for anomalies\n"
        self.info += fg(8)+"By"+self.rs+" Ciaran McNally ~ info@securit.ie\n"
        self.info += self.rs

    def show(self):
        print(self.top)
        print(self.mid)
        print(self.bottom)
        print(self.info)
