import pygame.event
import pygame
import random
import math

pygame.init()

class DrawInformation:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    GREY = 128, 128, 128
    GRADIENTS=[
        (128,128,128),
        (160,160,160),
        (192,192,192)
    ]

    BACKGROUND_COLOR = WHITE

    FONT=pygame.font.SysFont('comicsans',20)
    LARGE_FONT=pygame.font.SysFont('comicsans',40)
    SIDE_PAD = 100
    TOP_PAD = 150

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualization")
        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.max_val = max(lst)
        self.min_val = min(lst)

        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
        self.start_x = self.SIDE_PAD // 2

def draw(draw_info,algo_name,ascending):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    title=draw_info.FONT.render(f"{algo_name} - {'Ascending'if ascending else 'Descending'}",1,draw_info.GREEN)
    draw_info.window.blit(title,(draw_info.width/2-title.get_width()/2,5))


    controls=draw_info.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending",1,draw_info.BLACK)
    draw_info.window.blit(controls,(draw_info.width/2-controls.get_width()/2,45))
   
    sorting=draw_info.FONT.render("I-Insertion Sort | B - Bubble Sort |  Q - Quick Sort | H - Heap Sort | S - Selection Sort" ,1,draw_info.BLACK)
    draw_info.window.blit(sorting,(draw_info.width/2-sorting.get_width()/2,75))
   
    draw_list(draw_info)
    pygame.display.update()

def draw_list(draw_info,color_position={},clear_bg=False):
    lst=draw_info.lst
    if clear_bg:
        clear_rect=(draw_info.SIDE_PAD//2,draw_info.TOP_PAD,draw_info.width-draw_info.SIDE_PAD,draw_info.height-draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window,draw_info.BACKGROUND_COLOR,clear_rect)
    
    for i,val in enumerate(lst):
        x=draw_info.start_x+i*draw_info.block_width
        y=draw_info.height-(val-draw_info.min_val)*draw_info.block_height
        color=draw_info.GRADIENTS[i%3]
        if i in color_position:
            color=color_position[i]
        pygame.draw.rect(draw_info.window,color,(x,y,draw_info.block_width,draw_info.height))

    if(clear_bg):
        pygame.display.update()
    
    
def generate_starting_list(n, min_val, max_val):
    lst = []
    for _ in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)
    return lst

def bubble_sort(draw_info,ascending=True):
    lst=draw_info.lst
    for i in range(len(lst)-1):
        for j in range(len(lst)-1-i):
            num1=lst[j]
            num2=lst[j+1]
            if(num1>num2 and ascending) or (num1 <num2 and not ascending):
                lst[j],lst[j+1]=lst[j+1],lst[j]
                draw_list(draw_info,{j:draw_info.GREEN,j+1:draw_info.RED},True)

                yield True  #yield is going to pause but store the current state of the function so the next time i call this generator its going to run from where it left

    return lst


def insertion_sort(draw_info,ascending):
    lst=draw_info.lst
    for i in range(1,len(lst)):
        current=lst[i]
        j=i-1

        while(j>=0 and (lst[j]>current if ascending else lst[j]<current)):
             lst[j+1]=lst[j]
             draw_list(draw_info,{j:draw_info.GREEN,j+1:draw_info.RED},True)
             yield True
             j-=1
        
        lst[j+1]=current
        draw_list(draw_info,{j+1:draw_info.RED},True)
        yield True
    return lst










def quick_sort(draw_info, ascending=True):
    lst = draw_info.lst

    def partition(lst, low, high):
        pivot = lst[high]
        i = low - 1
        for j in range(low, high):
            if (lst[j] <= pivot and ascending) or (lst[j] >= pivot and not ascending):
                i += 1
                lst[i], lst[j] = lst[j], lst[i]
                draw_list(draw_info, {i: draw_info.GREEN, j: draw_info.RED}, True)
                yield True
        lst[i + 1], lst[high] = lst[high], lst[i + 1]
        draw_list(draw_info, {i + 1: draw_info.RED, high: draw_info.GREEN}, True)
        yield True
        return i + 1

    def sort(lst, low, high):
        if low < high:
            pi = yield from partition(lst, low, high)
            yield from sort(lst, low, pi - 1)
            yield from sort(lst, pi + 1, high)

    # Start quick sort
    yield from sort(lst, 0, len(lst) - 1)



def heapify(draw_info,lst,n,i,ascending=True):
    largest=i
    left=2*i+1
    right=2*i+2
    if left<n and ((lst[left]>lst[largest] and ascending)or (lst[left]<lst[largest] and not ascending)):
        largest=left
    if right<n and ((lst[right]>lst[largest] and ascending)or(lst[right]<lst[largest] and not ascending)):
        largest=right

    if largest !=i:
        lst[i],lst[largest]=lst[largest],lst[i]
        draw_list(draw_info,{i:draw_info.GREEN,largest:draw_info.RED},True)
        yield True 
        yield from heapify(draw_info,lst,n,largest,ascending)


def heap_sort(draw_info,ascending=True):
    lst=draw_info.lst
    n=len(lst)
    for i in range(n // 2 - 1, -1, -1):
        yield from heapify(draw_info, lst, n, i, ascending)
    for i in range(n - 1, 0, -1):
        lst[i], lst[0] = lst[0], lst[i]
        draw_list(draw_info, {0: draw_info.GREEN, i: draw_info.RED}, True)
        yield True
        yield from heapify(draw_info, lst, i, 0, ascending)

def selection_sort(draw_info, ascending=True):
    lst = draw_info.lst
    for i in range(len(lst)):
        min_index = i
        for j in range(i + 1, len(lst)):
            if (lst[j] < lst[min_index] and ascending) or (lst[j] > lst[min_index] and not ascending):
                min_index = j
        lst[i], lst[min_index] = lst[min_index], lst[i]
        draw_list(draw_info, {i: draw_info.GREEN, min_index: draw_info.RED}, True)
        yield True
    return lst


def main():
    run = True
    clock = pygame.time.Clock()
    n=50
    min_val=0
    max_val=100

    lst = generate_starting_list(50, 10, 100)
    draw_info = DrawInformation(800, 600, lst)
    sorting=False
    ascending =True
    sorting_algorithm=bubble_sort
    sorting_algo_name="Bubble Sort"
    sorting_algorithm_generator=None

    while run:
        clock.tick(60)

        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting=False
        else:
            draw(draw_info,sorting_algo_name,ascending)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type!=pygame.KEYDOWN:
                continue
            if event.key==pygame.K_r:#r to keep changing the list
                lst=generate_starting_list(n,min_val,max_val)
                draw_info.set_list(lst)
                sorting=False
            elif  event.key==pygame.K_SPACE and sorting==False:
               sorting=True
               sorting_algorithm_generator=sorting_algorithm(draw_info,ascending)
            elif  event.key==pygame.K_a and not sorting :
               ascending=True
            elif event.key==pygame.K_d and not sorting:
                ascending=False
            elif event.key==pygame.K_i and not sorting:
                sorting_algorithm=insertion_sort
                sorting_algo_name="Insertion Sort"
            elif event.key==pygame.K_b and not sorting:
                sorting_algorithm=bubble_sort
                sorting_algo_name="Bubble Sort"
            elif event.key == pygame.K_q and not sorting:
                sorting_algorithm = quick_sort
                sorting_algo_name = "Quick Sort"
            elif event.key == pygame.K_h and not sorting:
                sorting_algorithm = heap_sort
                sorting_algo_name = "Heap Sort"
            elif event.key == pygame.K_s and not sorting:
                sorting_algorithm = selection_sort
                sorting_algo_name = "Selection Sort"

             

    pygame.quit()


if __name__ == "__main__":
    main()
