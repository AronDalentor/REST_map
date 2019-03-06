import multiprocessing

def spawn(num, num2):
    print('Spawn # {} {}'.format(num, num2))

if __name__ == '__main__':
    for i in range(5):
        p = multiprocessing.Process(target=spawn, args=(i, i+1))
        p.start()