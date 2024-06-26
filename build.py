import asyncio

import embedded.compiler
import embedded.cpu
import embedded.cli
import embedded.microcontroller

import pathlib

async def build_stemmag0():
	mcu = embedded.microcontroller.get_mcus_from_string("STM32G030F6")[0]
	build = pathlib.Path("build").resolve()
	async with asyncio.TaskGroup() as tg:
		tg.create_task(mcu.generate_c_header("FLASH", build / "flash.h"))
		tg.create_task(mcu.generate_c_header("GPIOB", build / "gpiob.h"))
		tg.create_task(mcu.generate_c_header("I2C", build / "i2c.h"))
		tg.create_task(mcu.generate_c_header("RCC", build / "rcc.h"))
	compiler = embedded.compiler.Clang()
	await compiler.compile(mcu.cpu, "main.c", build / "main.o", ["-I build"])
	await compiler.link(mcu.cpu, [build / "main.o"], build / "main.elf", "linker.ld", ["-nostdlib"])

if __name__ == "__main__":
	embedded.cli.run(build_stemmag0)
