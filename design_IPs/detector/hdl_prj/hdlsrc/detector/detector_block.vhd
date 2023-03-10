-- -------------------------------------------------------------
-- 
-- File Name: hdl_prj\hdlsrc\detector\detector_block.vhd
-- Created: 2022-09-01 15:45:31
-- 
-- Generated by MATLAB 9.12 and HDL Coder 3.20
-- 
-- -------------------------------------------------------------


-- -------------------------------------------------------------
-- 
-- Module: detector_block
-- Source Path: detector/detector/detector
-- Hierarchy Level: 1
-- 
-- -------------------------------------------------------------
LIBRARY IEEE;
USE IEEE.std_logic_1164.ALL;
USE IEEE.numeric_std.ALL;
USE work.detector_pkg.ALL;

ENTITY detector_block IS
  PORT( clk                               :   IN    std_logic;
        reset                             :   IN    std_logic;
        enb                               :   IN    std_logic;
        xcorrSquareIn                     :   IN    std_logic_vector(38 DOWNTO 0);  -- sfix39
        acorrSquareIn                     :   IN    std_logic_vector(31 DOWNTO 0);  -- int32
        detectedRepeat                    :   OUT   std_logic;  -- ufix1
        cntDetectedSingle                 :   OUT   std_logic_vector(15 DOWNTO 0);  -- uint16
        cntDetectedRepeat                 :   OUT   std_logic_vector(15 DOWNTO 0)  -- uint16
        );
END detector_block;


ARCHITECTURE rtl OF detector_block IS

  -- Signals
  SIGNAL xcorrSquareIn_signed             : signed(38 DOWNTO 0);  -- sfix39
  SIGNAL acorrSquareIn_signed             : signed(31 DOWNTO 0);  -- int32
  SIGNAL cntDetectedSingle_tmp            : unsigned(15 DOWNTO 0);  -- uint16
  SIGNAL cntDetectedRepeat_tmp            : unsigned(15 DOWNTO 0);  -- uint16
  SIGNAL detectionHistory                 : std_logic_vector(0 TO 48);  -- ufix1 [49]
  SIGNAL cntDetectedSingle_reg            : unsigned(15 DOWNTO 0);  -- uint16
  SIGNAL cntDetectedRepeat_reg            : unsigned(15 DOWNTO 0);  -- uint16
  SIGNAL detectedRepeat_reg               : std_logic;  -- ufix1
  SIGNAL detectedSingle_reg               : std_logic;  -- ufix1
  SIGNAL detectionHistory_next            : std_logic_vector(0 TO 48);  -- ufix1 [49]
  SIGNAL cntDetectedSingle_reg_next       : unsigned(15 DOWNTO 0);  -- uint16
  SIGNAL cntDetectedRepeat_reg_next       : unsigned(15 DOWNTO 0);  -- uint16
  SIGNAL detectedRepeat_reg_next          : std_logic;  -- ufix1
  SIGNAL detectedSingle_reg_next          : std_logic;  -- ufix1

BEGIN
  xcorrSquareIn_signed <= signed(xcorrSquareIn);

  acorrSquareIn_signed <= signed(acorrSquareIn);

  detector_process : PROCESS (clk, reset)
  BEGIN
    IF reset = '0' THEN
      detectionHistory <= (OTHERS => '0');
      cntDetectedSingle_reg <= to_unsigned(16#0000#, 16);
      cntDetectedRepeat_reg <= to_unsigned(16#0000#, 16);
      detectedRepeat_reg <= '0';
      detectedSingle_reg <= '0';
    ELSIF clk'EVENT AND clk = '1' THEN
      IF enb = '1' THEN
        detectionHistory <= detectionHistory_next;
        cntDetectedSingle_reg <= cntDetectedSingle_reg_next;
        cntDetectedRepeat_reg <= cntDetectedRepeat_reg_next;
        detectedRepeat_reg <= detectedRepeat_reg_next;
        detectedSingle_reg <= detectedSingle_reg_next;
      END IF;
    END IF;
  END PROCESS detector_process;

  detector_output : PROCESS (acorrSquareIn_signed, cntDetectedRepeat_reg, cntDetectedSingle_reg,
       detectedRepeat_reg, detectedSingle_reg, detectionHistory,
       xcorrSquareIn_signed)
    VARIABLE detect : std_logic;
    VARIABLE c : signed(38 DOWNTO 0);
    VARIABLE t_0 : std_logic_vector(0 TO 48);
    VARIABLE t_1 : std_logic_vector(0 TO 48);
    VARIABLE cast : vector_of_signed64(0 TO 3);
  BEGIN
    detectionHistory_next <= detectionHistory;
    cntDetectedSingle_reg_next <= cntDetectedSingle_reg;
    cntDetectedRepeat_reg_next <= cntDetectedRepeat_reg;
    detectedRepeat_reg_next <= detectedRepeat_reg;
    detectedSingle_reg_next <= detectedSingle_reg;
    detect := '1';

    FOR k IN 0 TO 3 LOOP
      cast(k) := resize(to_signed(k, 32) & '0' & '0' & '0' & '0', 64);
      detect := detect AND detectionHistory(to_integer(resize(cast(k), 31)));
    END LOOP;

    IF detect = '1' THEN 
      cntDetectedRepeat_reg_next <= cntDetectedRepeat_reg + 1;
      detectedRepeat_reg_next <= '1';
    ELSE 
      detectedRepeat_reg_next <= '0';
    END IF;
    IF detectedSingle_reg = '1' THEN 
      t_1(0) := '1';
      t_1(1 TO 48) := detectionHistory(0 TO 47);
      detectionHistory_next <= t_1;
      cntDetectedSingle_reg_next <= cntDetectedSingle_reg + 1;
    ELSE 
      t_0(0) := '0';
      t_0(1 TO 48) := detectionHistory(0 TO 47);
      detectionHistory_next <= t_0;
    END IF;
    c := SHIFT_RIGHT(xcorrSquareIn_signed, 5);
    IF c > resize(acorrSquareIn_signed, 39) THEN 
      detectedSingle_reg_next <= '1';
    ELSE 
      detectedSingle_reg_next <= '0';
    END IF;
    detectedRepeat <= detectedRepeat_reg;
    cntDetectedSingle_tmp <= cntDetectedSingle_reg;
    cntDetectedRepeat_tmp <= cntDetectedRepeat_reg;
  END PROCESS detector_output;


  cntDetectedSingle <= std_logic_vector(cntDetectedSingle_tmp);

  cntDetectedRepeat <= std_logic_vector(cntDetectedRepeat_tmp);

END rtl;

