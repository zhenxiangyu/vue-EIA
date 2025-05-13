class NoisePoint {
  x: number
  y: number
  constructor(x: number, y: number) {
    this.x = x
    this.y = y
  }
}

class NoisePointGroup {
  width: number
  height: number
  noisePoints: Array<NoisePoint>
  constructor(width: number, height: number) {
    this.width = width
    this.height = height
    this.noisePoints = []
  }
}

class ZeroPoint {
  x: number
  y: number
  constructor(x: number, y: number) {
    this.x = x
    this.y = y
  }
}

class SensitivePoint {
  x: number
  y: number
  constructor(x: number, y: number) {
    this.x = x
    this.y = y
  }
}

export { ZeroPoint, NoisePoint, NoisePointGroup, SensitivePoint }
