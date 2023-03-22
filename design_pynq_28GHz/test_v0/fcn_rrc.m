function h = fcn_rrc(beta,t)
h = (sin((1-beta)*pi*t)+4*beta*t.*cos((1+beta)*pi*t))./ (pi*t.*(1-(4*beta*t).^2));
h(t==0) = 1 - beta*(1 - (4/pi));
h(t == 1/4/beta | t == -1/4/beta) = beta/sqrt(2)*((1+2/pi) * sin(pi/(4*beta)) + (1-2/pi) * cos(pi/(4*beta)));
h = h(:);
end