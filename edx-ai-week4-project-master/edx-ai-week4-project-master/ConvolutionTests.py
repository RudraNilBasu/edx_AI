from ABTestingBase import ABTestingBase
from ConvolutionKernel import ConvolutionKernel


class ConvolutionTests(ABTestingBase):
    def test_incorrect_dimensions_should_cause_exception(self):
        incorrect = [[1, 2], [1, 2]]
        with self.assertRaises(ValueError) as context:
            sut = ConvolutionKernel(incorrect)

    def test_can_create_kernel(self):
        correct = [[1, 2, 3], [1, 2, 3], [1, 2, 3]]
        sut = ConvolutionKernel(correct)
        self.assertIsNotNone(sut)

    def test_can_compute_identity_kernel(self):
        fg = self.create_random_fastgrid()
        sut = ConvolutionKernel([[0, 0, 0], [0, 1, 0], [0, 0, 0]])
        for y in range(4):
            for x in range(4):
                self.assertEqual(fg[x, y], sut.compute_point(x, y, fg))

    def test_can_compute_doubling_kernel(self):
        fg = self.create_random_fastgrid()
        sut = ConvolutionKernel([[0, 0, 0], [0, 2, 0], [0, 0, 0]])
        for y in range(4):
            for x in range(4):
                self.assertEqual(2 * fg[x, y], sut.compute_point(x, y, fg))

    def test_can_detect_edge(self):
        fg = self.create_fastgrid_from([
            0, 128, 64, 32,
            0, 128, 64, 32,
            0, 128, 64, 32,
            0, 128, 64, 32
        ])
        # Sobel Operator: https://en.wikipedia.org/wiki/Sobel_operator
        sut = ConvolutionKernel([[1, 0, -1],
                                 [2, 0, -2],
                                 [1, 0, -1]])
        new_array = sut.compute(fg)
        self.assertIsNotNone(new_array)

    def test_can_detect_edge_2(self):
        fg = self.create_fastgrid_from([
            0, 128, 0, 0,
            0, 128, 0, 0,
            0, 128, 0, 0,
            0, 128, 0, 0
        ])
        # Sobel Operator: https://en.wikipedia.org/wiki/Sobel_operator
        sut = ConvolutionKernel([[1, 0, -1],
                                 [2, 0, -2],
                                 [1, 0, -1]])
        new_array = sut.compute(fg)
        self.assertIsNotNone(new_array)


    def test_can_highlight_checkerboard(self):
        fg = self.create_fastgrid_from([
            2,  32, 32, 32,
            8,  16, 32, 32,
            32, 32, 32, 32,
            32, 32, 32, 32
        ])
        # Sobel Operator: https://en.wikipedia.org/wiki/Sobel_operator
        sut = ConvolutionKernel([[-1, -1, -1],
                                 [-1, +8, -1],
                                 [-1, -1, -1]])
        new_array = sut.compute(fg)
        self.assertIsNotNone(new_array)

    def test_can_highlight_blocking_tiles_in_corner(self):
        fg = self.create_fastgrid_from([
            2,  32, 32, 32,
            32, 32, 32, 32,
            32, 32, 32, 32,
            32, 32, 32, 32
        ])
        # Sobel Operator: https://en.wikipedia.org/wiki/Sobel_operator
        sut = ConvolutionKernel([[0, 0, 0],
                                 [0, +3, -1],
                                 [0, -1, -1]])
        new_array = sut.compute(fg)
        self.assertIsNotNone(new_array)

    def test_can_highlight_high_tiles_in_corner(self):
        fg = self.create_fastgrid_from([
            1024,  32, 32, 32,
            32, 32, 32, 32,
            32, 32, 32, 32,
            32, 32, 32, 32
        ])
        sut = ConvolutionKernel([[0, 0, 0],
                                 [0, +3, -1],
                                 [0, -1, -1]])
        new_array = sut.compute(fg)
        self.assertIsNotNone(new_array)

    def test_can_identify_gradient_lr(self):
        fg = self.create_fastgrid_from([
            64, 32, 16, 8,
            32, 32, 32, 32,
            32, 32, 32, 32,
            32, 32, 32, 32
        ])
        sut = ConvolutionKernel([[+0, +0, -0],
                                 [+1, +1, -1],
                                 [+0, +0, -0]])
        new_array = sut.compute(fg)

        self.assertIsNotNone(new_array)

    def diff(self, a1, a2):
        return [x-y for x,y in zip(a1, a2)]

    def test_can_highlight_stranded_high_tile(self):
        fg = self.create_fastgrid_from([
            32, 32, 32, 32,
            32, 32, 32, 32,
            32, 32, 128, 32,
            32, 32, 32, 32
        ])
        sut = ConvolutionKernel([[-0, +1, +0],
                                 [+1, -5, +1],
                                 [-0, +1, +0]])
        new_array = sut.compute(fg)
        self.assertIsNotNone(new_array)

    def test_can_compute_on_all_edges(self):
        self.fail("not implemented")

    def test_can_compute_on_all_corners(self):
        self.fail("not implemented")



