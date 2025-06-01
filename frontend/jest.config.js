/** @type {import('ts-jest').JestConfigWithTsJest} */
module.exports = {
    preset: 'ts-jest',            // use ts-jest to compile
    testEnvironment: 'node',       // or 'jsdom' if you need a browser-like DOM
    roots: ['<rootDir>/src'],      // where your source & tests live
    testMatch: [
      '**/__tests__/**/*.test.ts', // look for .test.ts under any __tests__ folder
    ],
    moduleFileExtensions: ['ts','js','json','node'],
    transform: {
      '^.+\\.tsx?$': 'ts-jest',    // transform .ts/.tsx via ts-jest
    }
  };