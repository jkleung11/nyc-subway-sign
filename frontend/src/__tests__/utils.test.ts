// @ts-ignore
jest.mock('../display/matrix', () => ({
  font: { stringWidth: jest.fn().mockReturnValue(0) },
  // matrix stub is not needed for processStopLabel tests
}));

import { Colors } from '../display/colors';
import {
    drawTrainLogo,
    processStopLabel

} from '../display/utils'

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

function makeMockMatrix() {
    // create an object with the matrix methods we want to assert are called
    return {
        clear: jest.fn(),
        fgColor: jest.fn(),
        drawText: jest.fn(),
        drawLine: jest.fn(),
        sync: jest.fn(),
        width: jest.fn().mockReturnValue(64)
    } as any;
}

describe ('drawTrainLogo', () => {
    let matrix: any

    beforeEach(() => {
        matrix = makeMockMatrix()
    })

    it('draws a train logo', () => {
        drawTrainLogo(matrix, 1, 1, 1, 'A');
        expect(matrix.clear).not.toHaveBeenCalled();
        expect(matrix.drawLine).toHaveBeenCalledTimes(9);
        expect(matrix.fgColor).toHaveBeenCalledWith(Colors.Blue);
        expect(matrix.drawText).toHaveBeenCalledWith('A', 3, 4);

    })

})