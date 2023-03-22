function [IQdata, h] =  fcn_singleCarrier(rho, symbols, Nover)
    n = [-21:1/Nover:21];
    h = fcn_rrc(rho,n);
    %h = sinc(n);
    h = h/norm(h);
    h = h(:);
    symbolsUp = upsample(symbols(:),Nover);
    IQdata = conv(h,symbolsUp);
end