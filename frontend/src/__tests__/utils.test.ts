// @ts-ignore
jest.mock('../display/matrix', () => ({
    font: { stringWidth: jest.fn().mockReturnValue(0) },
    // matrix stub is not needed for processStopLabel tests
}));

import { Colors } from '../display/colors';
import * as utils from '../display/utils'

describe('processStopLabel', () => {

    it('preserves short name', () => {
        expect(utils.processStopLabel('Manhattan', 'N')).toBe('Manhattan');
    });

    it('converts to uptown and downtown', () => {
        expect(utils.processStopLabel('a stop label that is tooooooo long', 'N')).toBe('Uptown');
        expect(utils.processStopLabel('another label that is too long', 'S')).toBe('Downtown');
    });

    it('throws an error for a bad direction', () => {
        expect(() => utils.processStopLabel('label', 'X')).toThrow("Invalid direction letter");
    });
});

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
};

describe('drawTrainLogo', () => {
    let matrix: any

    beforeEach(() => {
        matrix = makeMockMatrix()
    })

    it('draws a train logo', () => {
        utils.drawTrainLogo(matrix, 1, 1, 1, 'A');
        expect(matrix.clear).not.toHaveBeenCalled();
        expect(matrix.drawLine).toHaveBeenCalledTimes(9);
        expect(matrix.fgColor).toHaveBeenCalledWith(Colors.Blue);
        // our train name is written by turning off the LEDs
        expect(matrix.fgColor).toHaveBeenLastCalledWith(0x00000);
        expect(matrix.drawText).toHaveBeenCalledWith('A', 3, 4);

    })

});

describe('displayError', () => {
    let matrix: any;

    beforeEach(() => {
        matrix = makeMockMatrix();
    })

    it('displays error messages', () => {
        utils.displayError(matrix, utils.DisplayErrorType.ApiError);
        expect(matrix.clear).toHaveBeenCalledTimes(1);
        expect(matrix.drawText).toHaveBeenCalledWith("api error", 1, 2);
        expect(matrix.sync).toHaveBeenCalledTimes(1);
    })
});

describe('displayArrivals', () => {
    let matrix: any;
    let fakeArrival: any;

    beforeEach(() => {
        matrix = makeMockMatrix();
        fakeArrival = {
            route_id: "A",
            direction_label: "short label",
            direction_letter: "N",
            arrival_mins: 5
        };
    });

    it('draws logo, processes label, and displays text for one arival', () => {
        const slot = { logoX: 1, logoY: 2, logoWidth: 3, stopLabelX: 4, timeX: 5, messageY: 6 };
        utils.displayArrivals(matrix, "MyStop", fakeArrival);

        expect(matrix.clear).toHaveBeenCalledTimes(1);
        // need to display the direction
        expect(matrix.drawText).toHaveBeenCalledWith("short label", 9, 5);
        // need to draw the arrival time
        expect(matrix.drawText).toHaveBeenCalledWith("5min", 46, 5);
        // need to draw the stop name
        expect(matrix.drawText).toHaveBeenLastCalledWith("MyStop", 32, 26);

        expect(matrix.sync).toHaveBeenCalledTimes(1);

    });
});