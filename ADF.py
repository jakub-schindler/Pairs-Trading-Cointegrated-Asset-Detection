import numpy as np

def ADF(time_series, order):

	#The order must be large enough so that the X matrix (calculated later) is invertible. There are ways to go around this,
	#but im assuming that data pool is going to be large enough so that it won't cause any problems.

	if order >= (len(time_series) - 3)/2:
		raise Exception("Order too big for given data sample: maximal possible order is "+str( np.ceil((len(time_series) - 3)/2) - 1 ))
	elif order < 1:
		raise Exception('Order is smaller than 1')

	#We're going to linearly regress y_{t} = a*y_{t-1} + b_1*Δy_{t-1} + ... + b_p*Δy_{t-p} where p is ADF order

	y_1 = time_series[order:-1]

	dy = np.diff(time_series)

	y0 = np.diff(time_series)[order:]

	lagged_dy_matrix = np.column_stack([dy[order - p:-p] for p in range(1, order+1)])

	#N and k are number of used data points for fit and number of fitted parameters

	N = len(y0)
	k = order + 2

	#We get an equation y = X*θ + ε, where theta is a k-dimensional vector of regression coefficients
	#We can solve for θ = (X.T * X)^-1 * X.T * y
	#Coefficients variations are on the diagonal of the matrix 1/(m-k) * |y - X*theta|^2 * (X.T * X)^-1

	X = np.column_stack([np.ones(N), y_1, lagged_dy_matrix])

	XTX_inv = np.linalg.inv(X.T @ X)

	theta_hat = XTX_inv @ X.T @ y0

	residuals = y0 - X @ theta_hat

	RSS = residuals @ residuals

	cov_theta = RSS / (N-k) * XTX_inv

	#The adf statistic is found by taking the coefficient near the y_{t-1} term and dividing by its standard deviation

	adf_stat = theta_hat[1] / np.sqrt(np.diag(cov_theta))[1]

	#We're also returning the AIC value to choose the right order

	AIC = 2*k + N*np.log(RSS / N)

	return adf_stat, AIC

#A function that returns approximated critical values od ADF test. So far i've only implemented it so that it works for
#regression with a constant, no trend nad alpha = 0.05. I might expand it in the future.

def ADF_crit_values(N, alpha = 0.05,  const = True, trend = False):
	if alpha == 0.05:
		if const == True:
			if trend == False:
				t = -2.86154
				u = -2.8903
				v = -4.234
				w = -40.04
				return t + u/N + v / (N**2) + w / (N**3)
	else:
		raise Exception("No Data")
