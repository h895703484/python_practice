import random
import tkinter
'''
要求，
1 建立屏保程序，
2. 屏保是随机球，自己运动
3. 鼠标移动则清除

分析：
1， 需要一个ScreenSaver类，一个Ball的类
2. ScreenSaver：
	1.1: 需要一个canvas， 大小与屏幕一致
	1.2：程序已启动，就开始在屏幕上画小球，小球位置随机，会动，速度，方向随机
	1.3： 鼠标一移动，则程序退出
	1.4： 多少个小球，建议允许输入
2. RandomBall：
	2.1： 大小，颜色，出现位置，运动方向，速度，完全随机
	2.2： 球就有移动功能，可以被调用
'''

class RandomBall:
    def __init__(self, canvas, scrnwidth, scrnheight):
        self.canvas = canvas

        self.xpos = random.randint(10, int(scrnwidth))
        self.ypos = random.randint(10, int(scrnheight))

        self.xvelocity = random.randint(4,20)
        self.yvelocity = random.randint(4,20)

        self.scrnwidth = scrnwidth
        self.scrnheight = scrnheight

        self.radius = random.randint(20,120)

        c = lambda : random.randint(0,255)
        self.color = '#%02x%02x%02x'%(c(),c(),c())

    def create_ball(self):

        x1 = self.xpos - self.radius
        y1 = self.ypos - self.radius

        x2 = self.xpos + self.radius
        y2 = self.ypos + self.radius

        self.item = self.canvas.create_oval(x1,y1,x2,y2, fill=self.color, outline=self.color)

    def move_ball(self):
        self.xpos += self.xvelocity
        self.ypos += self.yvelocity

        if self.ypos >= self.scrnheight - self.radius:
           self.yvelocity = - self.yvelocity

        if self.ypos <= self.radius:
            self.yvelocity = abs(self.yvelocity)

        if self.xpos >= self.scrnwidth - self.radius or self.xpos <= self.radius:
            self.xvelocity = - self.xvelocity

        self.canvas.move(self.item, self.xvelocity, self.yvelocity)

class ScreenSaver:
    balls = []

    def __init__(self,num_balls):
        self.root = tkinter.Tk()
        # 取消边框
        self.root.overrideredirect(1)
        # 任何鼠标移动
        self.root.bind('<Motion>', self.myquit)

        w,h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.canvas = tkinter.Canvas(self.root, width=w, height=h )
        self.canvas.pack()

        for i in range(num_balls ):
            ball = RandomBall(self.canvas, scrnwidth=w, scrnheight=h)
            ball.create_ball()
            self.balls.append(ball)

        self.run_screen_saver()
        self.root.mainloop()

    def run_screen_saver(self):
        for ball in self.balls:
            ball.move_ball()
        self.canvas.after(200, self.run_screen_saver)

    def myquit(self,event):
        self.root.destroy()

if __name__ == "__main__":
    ScreenSaver(12)