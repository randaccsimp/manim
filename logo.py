#!/usr/bin/env python

from manimlib.imports import *
from random import shuffle, randrange

class Logo(Scene):
    def construct(self):
        # ======= params of the logo =======
        # Dimension of the maze
        w = 11
        h = 11
        dim = max(w,h)
        #random seed
        random.seed ()
        #Scale of the maze
        scale = 3.0
        #Noise added on the line coordinate
        eps = 0.015

        
        # ======= Making the maze =======
        # First step : Find a code that creates a maze
        # from http://rosettacode.org/wiki/Maze_generation#Python
        # Border are stored into a list of list
        # First dim : vertical coordinate
        # Second    : horizontal coordinate        

        # 2d visibility array  
        vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]
        # Vertical border 
        ver = [["|  "] * w + ['|'] for _ in range(h)] + [[]]
        # Horizontal border
        hor = [["+--"] * w + ['+'] for _ in range(h + 1)]
        # Walk fun
        def walk(x, y):
            vis[y][x] = 1
            d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
            shuffle(d)
            for (xx, yy) in d:
                if vis[yy][xx]: continue
                if xx == x: hor[max(y, yy)][x] = "+  "
                if yy == y: ver[y][max(x, xx)] = "   "
                walk(xx, yy)
        walk(randrange(w), randrange(h))
        # Adding the entrance / exit
        hor[0][int(w/2)] = '+  '
        hor[h][int(w/2)] = '+  '
        # Print it for debug
        s = ""
        for (a, b) in zip(hor, ver):
            s += ''.join(a + ['\n'] + b + ['\n'])
        print(s)
        

        # ======= Extracting the line of the maze =======
        # Create a maze centered at (0,0)
        line = []
        do_line=False
        ss=0
        # Create the horizontal line
        for hh in range(h+1) :
            for ww in range(w+1):
                # If we are on a wall and we are not drawing a line,
                # This is the begining, save the horizonal coordinate
                if hor[hh][ww] == "+--" and (not do_line) :
                    ss = ww
                    do_line = True
                # If we find a bordel of a line and we are actually on a line
                if (hor[hh][ww] == "+  " or hor[hh][ww] == '+') and do_line:
                    do_line = False
                    # Save the line.
                    ll = Line(np.array([((ss/dim)-0.5)*scale + random.uniform(-eps,eps),
                                        ((hh/dim)-0.5)*scale + random.uniform(-eps,eps),0]),
                              np.array([((ww/dim)-0.5)*scale + random.uniform(-eps,eps) ,
                                        ((hh/dim)-0.5)*scale + random.uniform(-eps,eps),0]),
                              color=WHITE)
                    line.append(ll);

        # Create the vertical line
        # There is no final border, the last case should be taken into account.
        def is_wall(tt) :
            return (tt == "|" or tt == "|  ")
        do_line = False
        ss = 0
        for ww in range(w+1) :
            for hh in range(h) :
                if (is_wall(ver[hh][ww]) and (not do_line)) :
                    ss = hh
                    do_line = True
                if ((ver[hh][ww] == "   ") and do_line ) or (hh == (h-1) and is_wall(ver[hh][ww])) :
                    pad = 0
                    # If there is a line and this is the last element
                    if ((hh == (h-1) and is_wall(ver[hh][ww]))) : 
                        pad = 1
                    ll = Line(np.array([((ww/dim)-0.5)*scale + random.uniform(-eps,eps),
                                        ((ss/dim)-0.5)*scale + random.uniform(-eps,eps),0]),
                              np.array([((ww/dim)-0.5)*scale + random.uniform(-eps,eps),
                                        (((hh+pad)/dim)-0.5)*scale + random.uniform(-eps,eps),0]),
                              color=WHITE)
                    line.append(ll);
                    do_line = False
            ss=0
            do_line=False

        # Shuffle the line array
        random.shuffle(line)
        for ll in line :
            ll.shift((scale/3)*UP)

        # Create two groupes of line
        # Divide the list into n partitions
        def chunks(lst, n):
            for i in range(0, len(lst), n):
                yield lst[i:i + n]
        line_c = chunks(line,int(len(line)/2) +1)

        # Create the arrow and its background
        tip = Arrow(np.array([-scale,scale/3,0]),np.array([scale,scale/3,0]),color = BLUE)
        rect = SurroundingRectangle(tip, color=BLACK)
        rect.set_fill(BLACK, opacity=1)
        rect.set_stroke(width=0)

        # Create Manim group of objects
        vg1 = VGroup(*next(line_c))
        vg2 = VGroup(*next(line_c))        
        vg3 = VGroup(vg1,vg2,rect,tip)


        
        ## ======= starting the animation ============
        # Start showing the two groupe of line
        for lll in [vg1,vg2] :
            self.play(*[
                ShowCreation(ll, run_time = 1.0)
                for ll in lll
            ])
        
        # Add the background rectangle
        self.add(rect)
        # Draw the arrow
        self.play(Write(tip),run_time = 1.5)
        # Rotation of the maze and arrow
        self.play(vg3.rotate,25*DEGREES,about_point=np.array([0,0]))
        # Drawing the text
        title1=TextMobject("Random Access").next_to(Point(np.array([0,-scale/3,0])),DOWN)
        title1.scale(1.6)
        title2=TextMobject("Simplicity").next_to(title1,DOWN)
        title2.scale(1.8)
        self.play(Write(title1),Write(title2),run_time = 1.5)
        self.wait(3)




        
