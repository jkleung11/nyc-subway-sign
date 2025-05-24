// @ts-ignore
jest.mock('../display/matrix', () => ({
  font: { stringWidth: jest.fn().mockReturnValue(0) },
  // matrix stub is not needed for processStopLabel tests
}));
import { processStopLabel } from '../display/utils'

describe('processStopLabel', () => {
    
    it('preserves short name', () => {
        expect(processStopLabel('Manhattan', 'N')).toBe('Manhattan');
    });

    it('converts to uptown and downtown', () => {
        expect(processStopLabel('a stop label that is tooooooo long', 'N')).toBe('Uptown');
        expect(processStopLabel('another label that is too long', 'S')).toBe('Downtown');
    });

    it ('throws an error for a bad direction', () => {
        expect(() => processStopLabel('label', 'X')).toThrow("Invalid direction letter");
    });
}) 