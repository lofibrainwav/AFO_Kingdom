import React, { useState, useEffect, useCallback } from 'react';
import { X, RefreshCw, Calculator, Equal, Keyboard, Delete, Send } from 'lucide-react';
import { useApp } from '../context/AppContext';

export const CalculatorWidget: React.FC = () => {
  const { isCalculatorOpen, toggleCalculator, setCalculatorTotal, addToChat } = useApp();
  const [display, setDisplay] = useState('0');
  const [history, setHistory] = useState<string>('');
  const [prevValue, setPrevValue] = useState<number | null>(null);
  const [operator, setOperator] = useState<string | null>(null);
  const [waitingForOperand, setWaitingForOperand] = useState(false);
  const [lastKey, setLastKey] = useState<string | null>(null);

  const inputDigit = useCallback((digit: string) => {
    if (waitingForOperand) {
      setDisplay(digit);
      setWaitingForOperand(false);
    } else {
      setDisplay(prev => prev === '0' ? digit : prev + digit);
    }
  }, [waitingForOperand]);

  const calculate = (prev: number, next: number, op: string) => {
    switch (op) {
      case '+': return prev + next;
      case '-': return prev - next;
      case '*': return prev * next;
      case '/': return prev / next;
      default: return next;
    }
  };

  const performOperation = useCallback((nextOperator: string) => {
    const inputValue = parseFloat(display.replace(/,/g, ''));
    if (prevValue === null) {
      setPrevValue(inputValue);
    } else if (operator) {
      const currentValue = prevValue || 0;
      const newValue = calculate(currentValue, inputValue, operator);
      setPrevValue(newValue);
      setDisplay(String(newValue));
      setCalculatorTotal(newValue);
    }
    setWaitingForOperand(true);
    setOperator(nextOperator);
    setHistory(`${inputValue} ${nextOperator}`);
  }, [display, prevValue, operator, setCalculatorTotal]);

  const handleEqual = useCallback(() => {
    if (!operator || prevValue === null) return;
    const inputValue = parseFloat(display.replace(/,/g, ''));
    const result = calculate(prevValue, inputValue, operator);
    setDisplay(String(result));
    setHistory('');
    setPrevValue(null);
    setOperator(null);
    setWaitingForOperand(true);
    setCalculatorTotal(result);
  }, [display, operator, prevValue, setCalculatorTotal]);

  const handleClear = useCallback(() => {
    setDisplay('0');
    setPrevValue(null);
    setOperator(null);
    setWaitingForOperand(false);
    setHistory('');
    setCalculatorTotal(0);
  }, [setCalculatorTotal]);

  const handleBackspace = useCallback(() => {
      if (waitingForOperand) return;
      setDisplay(prev => {
          if (prev.length > 1) return prev.slice(0, -1);
          return '0';
      });
  }, [waitingForOperand]);

  const handleSendToAgent = () => {
      addToChat(`Calculated Result: ${display}`, 'user');
      toggleCalculator();
  };

  useEffect(() => {
      if (!isCalculatorOpen) return;
      const handleKeyDown = (e: KeyboardEvent) => {
          const key = e.key;
          if (['Enter', ' ', 'ArrowUp', 'ArrowDown'].includes(key)) e.preventDefault();
          setLastKey(key);
          setTimeout(() => setLastKey(null), 150);
          if (/[0-9]/.test(key)) inputDigit(key);
          else if (['+', '-', '*', '/'].includes(key)) performOperation(key);
          else if (key === 'Enter' || key === '=') handleEqual();
          else if (key === 'Escape') handleClear();
          else if (key === 'Backspace') handleBackspace();
          else if (key === '.') inputDigit('.');
      };
      window.addEventListener('keydown', handleKeyDown);
      return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isCalculatorOpen, inputDigit, performOperation, handleEqual, handleClear, handleBackspace]);

  if (!isCalculatorOpen) return null;

  const formatDisplay = (val: string) => {
    const num = parseFloat(val);
    if (isNaN(num)) return 'Error';
    return num.toLocaleString('en-US', { maximumFractionDigits: 6 });
  };

  const getBtnClass = (btnKey: string, baseClass: string) => {
      const isActive = lastKey === btnKey || (btnKey === '=' && lastKey === 'Enter');
      return `${baseClass} ${isActive ? 'brightness-125 ring-2 ring-inset ring-white/20' : ''}`;
  };

  return (
    <div className="fixed bottom-24 left-6 w-80 bg-slate-900 rounded-3xl shadow-2xl border border-slate-700 overflow-hidden z-[60] animate-slide-down font-mono touch-none">
      <div className="bg-slate-800 p-4 flex justify-between items-center border-b border-slate-700 cursor-move select-none">
        <div className="flex items-center gap-2 text-emerald-400">
           <Calculator size={18} />
           <span className="text-sm font-bold tracking-wider">CPA CALC</span>
        </div>
        <div className="flex items-center gap-3">
             <div className="flex items-center gap-1 text-[10px] text-slate-500 bg-slate-900/50 px-2 py-1 rounded border border-slate-700/50">
                <Keyboard size={10} /> 
                <span className="hidden sm:inline">Numpad</span>
             </div>
            <button onClick={handleClear} className="text-slate-400 hover:text-white transition-colors"><RefreshCw size={14}/></button>
            <button onClick={toggleCalculator} className="text-slate-400 hover:text-red-400 transition-colors"><X size={16}/></button>
        </div>
      </div>

      <div className="p-6 bg-slate-900 text-right relative">
        <div className="text-slate-500 text-xs h-4 mb-1 truncate">{history}</div>
        <div className="text-4xl text-white font-light tracking-tight truncate">
            {formatDisplay(display)}
        </div>
        {parseFloat(display) !== 0 && (
            <button onClick={handleSendToAgent} className="absolute bottom-2 left-2 p-2 bg-blue-600/20 hover:bg-blue-600 text-blue-400 hover:text-white rounded-full transition-colors" title="Send to Chat">
                <Send size={14} />
            </button>
        )}
      </div>

      <div className="grid grid-cols-4 gap-px bg-slate-700">
         {['C', '⌫', '%', '/'].map((btn) => (
             <button 
                key={btn} 
                onClick={() => {
                    if (btn === 'C') handleClear();
                    else if (btn === '⌫') handleBackspace();
                    else performOperation(btn);
                }} 
                className={getBtnClass(btn === '⌫' ? 'Backspace' : btn === 'C' ? 'Escape' : btn, "bg-slate-800 hover:bg-slate-700 text-slate-300 p-4 text-sm font-medium transition-all active:bg-slate-600")}
             >
                 {btn === '⌫' ? <Delete size={18} className="mx-auto"/> : btn}
             </button>
         ))}
         {['7', '8', '9', '*'].map((btn) => (
             <button key={btn} onClick={() => ['*'].includes(btn) ? performOperation(btn) : inputDigit(btn)} className={getBtnClass(btn, `p-4 text-lg font-medium transition-all active:bg-slate-600 ${['*'].includes(btn) ? 'bg-slate-800 text-emerald-400 hover:bg-slate-700' : 'bg-slate-800 text-white hover:bg-slate-700'}`)}>{btn}</button>
         ))}
         {['4', '5', '6', '-'].map((btn) => (
             <button key={btn} onClick={() => ['-'].includes(btn) ? performOperation(btn) : inputDigit(btn)} className={getBtnClass(btn, `p-4 text-lg font-medium transition-all active:bg-slate-600 ${['-'].includes(btn) ? 'bg-slate-800 text-emerald-400 hover:bg-slate-700' : 'bg-slate-800 text-white hover:bg-slate-700'}`)}>{btn}</button>
         ))}
         {['1', '2', '3', '+'].map((btn) => (
             <button key={btn} onClick={() => ['+'].includes(btn) ? performOperation(btn) : inputDigit(btn)} className={getBtnClass(btn, `p-4 text-lg font-medium transition-all active:bg-slate-600 ${['+'].includes(btn) ? 'bg-slate-800 text-emerald-400 hover:bg-slate-700' : 'bg-slate-800 text-white hover:bg-slate-700'}`)}>{btn}</button>
         ))}
         {['0', '.', '=', ''].map((btn, idx) => (
             <button key={idx} onClick={() => btn === '=' ? handleEqual() : btn === '' ? {} : inputDigit(btn)} className={getBtnClass(btn === '=' ? 'Enter' : btn, `${btn === '0' ? 'col-span-2' : ''} ${btn === '=' ? 'bg-emerald-600 text-white hover:bg-emerald-500' : 'bg-slate-800 text-white hover:bg-slate-700'} p-4 text-lg font-medium transition-all active:brightness-110`)}>{btn === '=' ? <Equal size={20} className="mx-auto"/> : btn}</button>
         ))}
      </div>
    </div>
  );
};