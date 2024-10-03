import { LedMatrix, GpioMapping, Font } from "rpi-led-matrix";

const matrix = new LedMatrix({
  ...LedMatrix.defaultMatrixOptions(),
  rows: 32, 
  cols: 64,
  brightness: 50,
  chainLength: 1,
  hardwareMapping: GpioMapping.AdafruitHat,
  showRefreshRate: true
}, {
  ...LedMatrix.defaultRuntimeOptions(),
  gpioSlowdown: 4
})

const font = new Font('tom-thumb', 'fonts/tom-thumb.bdf');
matrix.font(font);

export {matrix, font};