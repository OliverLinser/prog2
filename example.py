from time import perf_counter as pc
from time import sleep as pause
import multiprocessing as mp
import concurrent.futures as future

def runner(n):
    print("Performing a costly function")
    pause(n)
    return f"Function {n} has completed"



# if __name__ == "__main__":
#     start = pc()
#     p1 = mp.Process(target=runner)
#     p2 = mp.Process(target=runner)

#     p1.start()
#     p2.start()
#     p1.join()
#     p2.join()
#     end = pc()
#     print(f"Process took {round(end-start, 2)} seconds")

if __name__ == "__main__":
    start = pc()

    with future.ThreadPoolExecutor() as ex:
        p= [5, 4, 3, 2, 1]
        results = ex.map(runner, p)
        for r in results:
            print(r)
    end = pc()
    print(f"Process took {round(end-start, 2)} seconds")

