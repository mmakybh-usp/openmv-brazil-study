import sensor, image, time

sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(time=2000)

def stats(us_list):
    us_list = sorted(us_list)
    n = len(us_list)
    mean = sum(us_list) / n
    med = us_list[n//2]
    p90 = us_list[int(n*0.9)]
    return mean, med, p90, max(us_list), min(us_list)

def benchmark(fn, name, n=20):
    times = []
    for _ in range(n):
        img = sensor.snapshot()
        t0 = time.ticks_us()
        fn(img)
        t1 = time.ticks_us()
        dt = time.ticks_diff(t1, t0)
        times.append(dt)
        print("%s,%d,raw" % (name, dt))  # cada valor cru
    mean, med, p90, tmax, tmin = stats(times)
    print("%s,%.0f,mean" % (name, mean))
    print("%s,%.0f,median" % (name, med))
    print("%s,%.0f,p90" % (name, p90))
    print("%s,%.0f,max" % (name, tmax))
    print("%s,%.0f,min" % (name, tmin))

# Funções de teste
def none(img): pass
def edge_simple(img): img.find_edges(image.EDGE_SIMPLE, threshold=(50,80))
def edge_canny(img): img.find_edges(image.EDGE_CANNY, threshold=(50,80))
def gaussian(img): img.gaussian(1)

# Cabeçalho CSV
print("operacao,tempo_us,tipo")

benchmark(none, "baseline")
benchmark(edge_simple, "EDGE_SIMPLE")
benchmark(edge_canny, "EDGE_CANNY")
benchmark(gaussian, "GAUSSIAN")
