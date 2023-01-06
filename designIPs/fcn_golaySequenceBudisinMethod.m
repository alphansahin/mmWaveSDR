% IDDC
% Alphan Sahin
% 802.11ad Golay Sequence Generation based on Busidin's Method
% Budisin, S.Z., "New complementary pairs of sequences," Electronics Letters , vol.26, no.13, pp.881,883, 21 June 1990
% w,d are the sequence paramenters, i is the stream index

function [Ga, Gb] = fcn_golaySequenceBudisinMethod(w, d, i)
    M = numel(d);
    
    Ga3_i = [+1, +1, -1].';
    Gb3_i = [+1, +1i, +1].';
    
    if i == 0
        Ga = 1;
        Gb = 1;
    elseif mod(i,2) == 1
        Ga = flipud(Ga3_i);
        Gb = flipud(Gb3_i);  
    else
        Ga = conj(Gb3_i);
        Gb = -conj(Ga3_i);  
    end

    a0 = [Ga; zeros(sum(d),1)];
    b0 = [Gb; zeros(sum(d),1)];
        
    
    for it=1:M
        a0p = a0;
        b0p = b0;

        a0 = w(it)*a0p + [zeros(d(it),1); b0p(1:end-d(it))];
        b0 = w(it)*a0p - [zeros(d(it),1); b0p(1:end-d(it))];
    end
    
    if i == 0
        Ga = flipud(a0);
        Gb = flipud(b0);
    else
        Ga = conj(flipud(a0));
        Gb = conj(flipud(b0));
    end
end