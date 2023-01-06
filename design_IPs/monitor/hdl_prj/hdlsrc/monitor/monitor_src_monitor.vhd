-- -------------------------------------------------------------
-- 
-- File Name: hdl_prj\hdlsrc\monitor\monitor_src_monitor.vhd
-- Created: 2022-08-29 17:43:08
-- 
-- Generated by MATLAB 9.12 and HDL Coder 3.20
-- 
-- 
-- -------------------------------------------------------------
-- Rate and Clocking Details
-- -------------------------------------------------------------
-- Model base rate: 1
-- Target subsystem base rate: 1
-- 
-- 
-- Clock Enable  Sample Time
-- -------------------------------------------------------------
-- ce_out        1
-- -------------------------------------------------------------
-- 
-- 
-- Output Signal                 Clock Enable  Sample Time
-- -------------------------------------------------------------
-- dataWrite0                    ce_out        1
-- dataWrite1                    ce_out        1
-- dataWrite2                    ce_out        1
-- dataWrite3                    ce_out        1
-- dataWrite4                    ce_out        1
-- dataWrite5                    ce_out        1
-- dataWrite6                    ce_out        1
-- dataWrite7                    ce_out        1
-- dataReadAXI0                  ce_out        1
-- dataReadAXI1                  ce_out        1
-- dataReadAXI2                  ce_out        1
-- dataReadAXI3                  ce_out        1
-- dataReadAXI4                  ce_out        1
-- dataReadAXI5                  ce_out        1
-- dataReadAXI6                  ce_out        1
-- dataReadAXI7                  ce_out        1
-- -------------------------------------------------------------
-- 
-- -------------------------------------------------------------


-- -------------------------------------------------------------
-- 
-- Module: monitor_src_monitor
-- Source Path: monitor/monitor
-- Hierarchy Level: 0
-- 
-- -------------------------------------------------------------
LIBRARY IEEE;
USE IEEE.std_logic_1164.ALL;
USE IEEE.numeric_std.ALL;

ENTITY monitor_src_monitor IS
  PORT( clk                               :   IN    std_logic;
        reset                             :   IN    std_logic;
        clk_enable                        :   IN    std_logic;
        dataWriteAXI0                     :   IN    std_logic_vector(31 DOWNTO 0);  -- uint32
        dataWriteAXI1                     :   IN    std_logic_vector(31 DOWNTO 0);  -- uint32
        dataWriteAXI2                     :   IN    std_logic_vector(31 DOWNTO 0);  -- uint32
        dataWriteAXI3                     :   IN    std_logic_vector(31 DOWNTO 0);  -- uint32
        dataWriteAXI4                     :   IN    std_logic_vector(31 DOWNTO 0);  -- uint32
        dataWriteAXI5                     :   IN    std_logic_vector(31 DOWNTO 0);  -- uint32
        dataWriteAXI6                     :   IN    std_logic_vector(31 DOWNTO 0);  -- uint32
        dataWriteAXI7                     :   IN    std_logic_vector(31 DOWNTO 0);  -- uint32
        dataRead0                         :   IN    std_logic_vector(31 DOWNTO 0);  -- uint32
        dataRead1                         :   IN    std_logic_vector(31 DOWNTO 0);  -- uint32
        dataRead2                         :   IN    std_logic_vector(31 DOWNTO 0);  -- uint32
        dataRead3                         :   IN    std_logic_vector(31 DOWNTO 0);  -- uint32
        dataRead4                         :   IN    std_logic_vector(31 DOWNTO 0);  -- uint32
        dataRead5                         :   IN    std_logic_vector(31 DOWNTO 0);  -- uint32
        dataRead6                         :   IN    std_logic_vector(31 DOWNTO 0);  -- uint32
        dataRead7                         :   IN    std_logic_vector(31 DOWNTO 0);  -- uint32
        ce_out                            :   OUT   std_logic;
        dataWrite0                        :   OUT   std_logic_vector(31 DOWNTO 0);  -- uint32
        dataWrite1                        :   OUT   std_logic_vector(31 DOWNTO 0);  -- uint32
        dataWrite2                        :   OUT   std_logic_vector(31 DOWNTO 0);  -- uint32
        dataWrite3                        :   OUT   std_logic_vector(31 DOWNTO 0);  -- uint32
        dataWrite4                        :   OUT   std_logic_vector(31 DOWNTO 0);  -- uint32
        dataWrite5                        :   OUT   std_logic_vector(31 DOWNTO 0);  -- uint32
        dataWrite6                        :   OUT   std_logic_vector(31 DOWNTO 0);  -- uint32
        dataWrite7                        :   OUT   std_logic_vector(31 DOWNTO 0);  -- uint32
        dataReadAXI0                      :   OUT   std_logic_vector(31 DOWNTO 0);  -- uint32
        dataReadAXI1                      :   OUT   std_logic_vector(31 DOWNTO 0);  -- uint32
        dataReadAXI2                      :   OUT   std_logic_vector(31 DOWNTO 0);  -- uint32
        dataReadAXI3                      :   OUT   std_logic_vector(31 DOWNTO 0);  -- uint32
        dataReadAXI4                      :   OUT   std_logic_vector(31 DOWNTO 0);  -- uint32
        dataReadAXI5                      :   OUT   std_logic_vector(31 DOWNTO 0);  -- uint32
        dataReadAXI6                      :   OUT   std_logic_vector(31 DOWNTO 0);  -- uint32
        dataReadAXI7                      :   OUT   std_logic_vector(31 DOWNTO 0)  -- uint32
        );
END monitor_src_monitor;


ARCHITECTURE rtl OF monitor_src_monitor IS

  -- Component Declarations
  COMPONENT monitor_src_MATLAB_Function
    PORT( clk                             :   IN    std_logic;
          reset                           :   IN    std_logic;
          enb                             :   IN    std_logic;
          dataWriteAXI0                   :   IN    std_logic_vector(31 DOWNTO 0);  -- uint32
          dataWriteAXI1                   :   IN    std_logic_vector(31 DOWNTO 0);  -- uint32
          dataWriteAXI2                   :   IN    std_logic_vector(31 DOWNTO 0);  -- uint32
          dataWriteAXI3                   :   IN    std_logic_vector(31 DOWNTO 0);  -- uint32
          dataWriteAXI4                   :   IN    std_logic_vector(31 DOWNTO 0);  -- uint32
          dataWriteAXI5                   :   IN    std_logic_vector(31 DOWNTO 0);  -- uint32
          dataWriteAXI6                   :   IN    std_logic_vector(31 DOWNTO 0);  -- uint32
          dataWriteAXI7                   :   IN    std_logic_vector(31 DOWNTO 0);  -- uint32
          dataRead0                       :   IN    std_logic_vector(31 DOWNTO 0);  -- uint32
          dataRead1                       :   IN    std_logic_vector(31 DOWNTO 0);  -- uint32
          dataRead2                       :   IN    std_logic_vector(31 DOWNTO 0);  -- uint32
          dataRead3                       :   IN    std_logic_vector(31 DOWNTO 0);  -- uint32
          dataRead4                       :   IN    std_logic_vector(31 DOWNTO 0);  -- uint32
          dataRead5                       :   IN    std_logic_vector(31 DOWNTO 0);  -- uint32
          dataRead6                       :   IN    std_logic_vector(31 DOWNTO 0);  -- uint32
          dataRead7                       :   IN    std_logic_vector(31 DOWNTO 0);  -- uint32
          dataWrite0                      :   OUT   std_logic_vector(31 DOWNTO 0);  -- uint32
          dataWrite1                      :   OUT   std_logic_vector(31 DOWNTO 0);  -- uint32
          dataWrite2                      :   OUT   std_logic_vector(31 DOWNTO 0);  -- uint32
          dataWrite3                      :   OUT   std_logic_vector(31 DOWNTO 0);  -- uint32
          dataWrite4                      :   OUT   std_logic_vector(31 DOWNTO 0);  -- uint32
          dataWrite5                      :   OUT   std_logic_vector(31 DOWNTO 0);  -- uint32
          dataWrite6                      :   OUT   std_logic_vector(31 DOWNTO 0);  -- uint32
          dataWrite7                      :   OUT   std_logic_vector(31 DOWNTO 0);  -- uint32
          dataReadAXI0                    :   OUT   std_logic_vector(31 DOWNTO 0);  -- uint32
          dataReadAXI1                    :   OUT   std_logic_vector(31 DOWNTO 0);  -- uint32
          dataReadAXI2                    :   OUT   std_logic_vector(31 DOWNTO 0);  -- uint32
          dataReadAXI3                    :   OUT   std_logic_vector(31 DOWNTO 0);  -- uint32
          dataReadAXI4                    :   OUT   std_logic_vector(31 DOWNTO 0);  -- uint32
          dataReadAXI5                    :   OUT   std_logic_vector(31 DOWNTO 0);  -- uint32
          dataReadAXI6                    :   OUT   std_logic_vector(31 DOWNTO 0);  -- uint32
          dataReadAXI7                    :   OUT   std_logic_vector(31 DOWNTO 0)  -- uint32
          );
  END COMPONENT;

  -- Component Configuration Statements
  FOR ALL : monitor_src_MATLAB_Function
    USE ENTITY work.monitor_src_MATLAB_Function(rtl);

  -- Signals
  SIGNAL dataWrite0_tmp                   : std_logic_vector(31 DOWNTO 0);  -- ufix32
  SIGNAL dataWrite1_tmp                   : std_logic_vector(31 DOWNTO 0);  -- ufix32
  SIGNAL dataWrite2_tmp                   : std_logic_vector(31 DOWNTO 0);  -- ufix32
  SIGNAL dataWrite3_tmp                   : std_logic_vector(31 DOWNTO 0);  -- ufix32
  SIGNAL dataWrite4_tmp                   : std_logic_vector(31 DOWNTO 0);  -- ufix32
  SIGNAL dataWrite5_tmp                   : std_logic_vector(31 DOWNTO 0);  -- ufix32
  SIGNAL dataWrite6_tmp                   : std_logic_vector(31 DOWNTO 0);  -- ufix32
  SIGNAL dataWrite7_tmp                   : std_logic_vector(31 DOWNTO 0);  -- ufix32
  SIGNAL dataReadAXI0_tmp                 : std_logic_vector(31 DOWNTO 0);  -- ufix32
  SIGNAL dataReadAXI1_tmp                 : std_logic_vector(31 DOWNTO 0);  -- ufix32
  SIGNAL dataReadAXI2_tmp                 : std_logic_vector(31 DOWNTO 0);  -- ufix32
  SIGNAL dataReadAXI3_tmp                 : std_logic_vector(31 DOWNTO 0);  -- ufix32
  SIGNAL dataReadAXI4_tmp                 : std_logic_vector(31 DOWNTO 0);  -- ufix32
  SIGNAL dataReadAXI5_tmp                 : std_logic_vector(31 DOWNTO 0);  -- ufix32
  SIGNAL dataReadAXI6_tmp                 : std_logic_vector(31 DOWNTO 0);  -- ufix32
  SIGNAL dataReadAXI7_tmp                 : std_logic_vector(31 DOWNTO 0);  -- ufix32

BEGIN
  u_MATLAB_Function : monitor_src_MATLAB_Function
    PORT MAP( clk => clk,
              reset => reset,
              enb => clk_enable,
              dataWriteAXI0 => dataWriteAXI0,  -- uint32
              dataWriteAXI1 => dataWriteAXI1,  -- uint32
              dataWriteAXI2 => dataWriteAXI2,  -- uint32
              dataWriteAXI3 => dataWriteAXI3,  -- uint32
              dataWriteAXI4 => dataWriteAXI4,  -- uint32
              dataWriteAXI5 => dataWriteAXI5,  -- uint32
              dataWriteAXI6 => dataWriteAXI6,  -- uint32
              dataWriteAXI7 => dataWriteAXI7,  -- uint32
              dataRead0 => dataRead0,  -- uint32
              dataRead1 => dataRead1,  -- uint32
              dataRead2 => dataRead2,  -- uint32
              dataRead3 => dataRead3,  -- uint32
              dataRead4 => dataRead4,  -- uint32
              dataRead5 => dataRead5,  -- uint32
              dataRead6 => dataRead6,  -- uint32
              dataRead7 => dataRead7,  -- uint32
              dataWrite0 => dataWrite0_tmp,  -- uint32
              dataWrite1 => dataWrite1_tmp,  -- uint32
              dataWrite2 => dataWrite2_tmp,  -- uint32
              dataWrite3 => dataWrite3_tmp,  -- uint32
              dataWrite4 => dataWrite4_tmp,  -- uint32
              dataWrite5 => dataWrite5_tmp,  -- uint32
              dataWrite6 => dataWrite6_tmp,  -- uint32
              dataWrite7 => dataWrite7_tmp,  -- uint32
              dataReadAXI0 => dataReadAXI0_tmp,  -- uint32
              dataReadAXI1 => dataReadAXI1_tmp,  -- uint32
              dataReadAXI2 => dataReadAXI2_tmp,  -- uint32
              dataReadAXI3 => dataReadAXI3_tmp,  -- uint32
              dataReadAXI4 => dataReadAXI4_tmp,  -- uint32
              dataReadAXI5 => dataReadAXI5_tmp,  -- uint32
              dataReadAXI6 => dataReadAXI6_tmp,  -- uint32
              dataReadAXI7 => dataReadAXI7_tmp  -- uint32
              );

  ce_out <= clk_enable;

  dataWrite0 <= dataWrite0_tmp;

  dataWrite1 <= dataWrite1_tmp;

  dataWrite2 <= dataWrite2_tmp;

  dataWrite3 <= dataWrite3_tmp;

  dataWrite4 <= dataWrite4_tmp;

  dataWrite5 <= dataWrite5_tmp;

  dataWrite6 <= dataWrite6_tmp;

  dataWrite7 <= dataWrite7_tmp;

  dataReadAXI0 <= dataReadAXI0_tmp;

  dataReadAXI1 <= dataReadAXI1_tmp;

  dataReadAXI2 <= dataReadAXI2_tmp;

  dataReadAXI3 <= dataReadAXI3_tmp;

  dataReadAXI4 <= dataReadAXI4_tmp;

  dataReadAXI5 <= dataReadAXI5_tmp;

  dataReadAXI6 <= dataReadAXI6_tmp;

  dataReadAXI7 <= dataReadAXI7_tmp;

END rtl;
