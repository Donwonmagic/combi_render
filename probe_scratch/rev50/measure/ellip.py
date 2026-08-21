"""Ellipse-fit utilities: algebraic conic fit (Fitzgibbon) + geometry decode."""
import numpy as np

def fit_ellipse(x, y):
    x = np.asarray(x,float); y = np.asarray(y,float)
    mx, my = x.mean(), y.mean(); sx, sy = x.std(), y.std()
    u = (x-mx)/sx; v = (y-my)/sy
    D = np.column_stack([u*u, u*v, v*v, u, v, np.ones_like(u)])
    S = D.T@D
    C = np.zeros((6,6)); C[0,2]=2; C[2,0]=2; C[1,1]=-1
    import scipy.linalg as la
    w, V = la.eig(S, C)
    w = np.real(w)
    cand = [i for i in range(6) if np.isfinite(w[i]) and w[i] > 0]
    if not cand:  # fall back: min |w|
        cand = [int(np.argmin(np.abs(w)))]
    i = cand[int(np.argmin(w[cand]))]
    a = np.real(V[:,i])
    A,B,Cc,Dd,E,F = a
    # undo normalisation u=(x-mx)/sx
    A2 = A/sx**2
    B2 = B/(sx*sy)
    C2 = Cc/sy**2
    D2 = -2*A*mx/sx**2 - B*my/(sx*sy) + Dd/sx
    E2 = -B*mx/(sx*sy) - 2*Cc*my/sy**2 + E/sy
    F2 = A*mx**2/sx**2 + B*mx*my/(sx*sy) + Cc*my**2/sy**2 - Dd*mx/sx - E*my/sy + F
    return np.array([A2,B2,C2,D2,E2,F2])

def decode(c):
    A,B,C,D,E,F = c
    M = np.array([[A, B/2],[B/2, C]])
    den = B*B - 4*A*C
    x0 = (2*C*D - B*E)/den
    y0 = (2*A*E - B*D)/den
    Fc = A*x0*x0 + B*x0*y0 + C*y0*y0 + D*x0 + E*y0 + F
    ev, evec = np.linalg.eigh(M/(-Fc))
    if np.any(ev<=0): return None
    ax = 1/np.sqrt(ev)          # semi-axes
    order = np.argsort(-ax)
    ax = ax[order]; evec = evec[:,order]
    major, minor = ax[0], ax[1]
    theta = np.arctan2(evec[1,0], evec[0,0])   # major-axis direction
    return dict(x0=x0, y0=y0, a=major, b=minor, ang=theta,
                majdir=np.array([np.cos(theta), np.sin(theta)]),
                mindir=np.array([-np.sin(theta), np.cos(theta)]))

def resid(c, x, y):
    """approximate geometric residual (Sampson)."""
    A,B,C,D,E,F = c
    Q = A*x*x + B*x*y + C*y*y + D*x + E*y + F
    gx = 2*A*x + B*y + D; gy = B*x + 2*C*y + E
    return Q/np.sqrt(gx*gx+gy*gy+1e-12)
