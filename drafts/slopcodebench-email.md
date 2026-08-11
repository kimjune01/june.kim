# Email: Gabriel Orlanski <gorlanski@wisc.edu>

Subject: SlopCodeBench answer keys failing in the official image

Hi Gabriel,

You built SlopCodeBench to test whether agents can extend their own code as the spec changes. I audited the pinned release using your eval-snapshot command in the official Docker image.

Four answer keys fail their own tests, and the eight TypeScript checkpoints break on an unpinned npx toolchain. I filed the receipts as issue 27: https://github.com/SprocketLab/slop-code-bench/issues/27

Please say whether the dynamic_buffer failures reproduce on your side.

June
