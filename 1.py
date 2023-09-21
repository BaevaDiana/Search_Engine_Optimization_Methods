import numpy as np
import matplotlib.pyplot as plt

def f(x, y):
    return x**2 + y**2

def grad_f(x, y):
    return np.array([2*x, 2*y])

def gradient_descent(starting_point=None, iterations=10, learning_rate=0.1):
    if starting_point is None:
        starting_point = np.random.uniform(-5, 5, size=2)
    trajectory = [starting_point]
    for i in range(iterations):
        x = trajectory[-1]
        grad = grad_f(*x)
        new_x = x - learning_rate*grad
        trajectory.append(new_x)
    return np.array(trajectory)

traj = gradient_descent(iterations=1000)

x = np.linspace(-5, 5, 100)
y = np.linspace(-5, 5, 100)
X, Y = np.meshgrid(x, y)
Z = f(X,Y)

fig, ax = plt.subplots(figsize=(10,10))
ax.contour(X,Y,Z, levels=np.logspace(0, 5, 35), cmap='gray')
ax.plot(*traj.T, color='red')
plt.show()
