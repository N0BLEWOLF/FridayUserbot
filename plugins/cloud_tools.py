# File written by  @BilakshanP compiled by @Ramanveerji
import asyncio
import os
import shutil as sht
from main_startup.core.decorators import friday_on_cmd
from main_startup.helper_func.basic_helpers import edit_or_reply, get_text
from main_startup.helper_func.basic_helpers import edit_or_reply
from main_startup.core.startup_helpers import load_plugin

@friday_on_cmd(['ls'],
    cmd_help={
    "help": "lists files and folder in the specified directory",
    "example": "{ch}ls /plugins or {ch}ls /"
    })
async def list_files(client, message):
  plug = await edit_or_reply(message, "Processing...")
  text = get_text(message)
  if not text:
      await plug.edit("Please give me a valid input, check help menu to know more!")
  if not os.path.exists(text):
      await plug.edit(f"No match found for `{text}`")
  if os.path.exists(text):
      the_file =  str(os.listdir(f"./{text}"))
      the_file = the_file.replace("[", "**•** ")
      the_file = the_file.replace("]", "")
      the_file = the_file.replace("'", "`")
      the_file = the_file.replace(",", "\n•")
      await plug.edit(f"Files in `{text}` are : \n \n{the_file}")
      
@friday_on_cmd(["remove"],
    cmd_help={
    "help": "Removes files from the given directory",
    "example": "{ch}remove /download/...."
    })
async def remove_file(client, message):
    plug = await edit_or_reply(message, "Processing...")
    text = get_text(message)
    if not text:
        await plug.edit("Please give me a valid input, check help menu to know more!")

    if not os.path.exists(f"/{text}"):
        await plug.edit(f"No match found for {text}")

    if os.path.exists(f"/{text}"):
        await plug.edit(f"The file `{text}` has been removed successfully!!!")
        os.remove(f"/{text}")
        
@friday_on_cmd(["cdownload", "cd"],
    cmd_help={
    "help": "downloads any file to a custom directory",
    "example": "{ch}cdownload or {ch}cd /directory/path "
    })

async def custom_download(client, message):
    text = await edit_or_reply(message, "Processing...")
    dir = get_text(message)

    if not dir:
        await text.edit("Please specify the directory as well. Type `/` to download a file to the parent directory.")
        return

    if not message.reply_to_message:
       await text.edit("Reply to a file to download it.")
       return

    if not message.reply_to_message.document:
        await text.edit("Is it even a document?")
        return

    d_file_name = message.reply_to_message.document.file_name

    if os.path.exists(os.path.join(f"./{dir}", d_file_name)):
        await text.edit(f"This file already exists in the `{dir}` directory!")
        return

    await message.reply_to_message.download(file_name=f"./{dir}")
    
    await text.edit(f"Sucessfully downloaded `{d_file_name}` to the `{dir}` directory!")
    
@friday_on_cmd(["sendfile", "sf"],
    cmd_help={
    "help": "sends any file from the directory",
    "example": "{ch}sendfile /plugins/sendfile.py or {ch}sf <file path>"
    })
async def send_file(client, message):
  plug = await edit_or_reply(message, "Processing...")
  text = get_text(message)
  if not text:
      await plug.edit("Please give me a valid input, check help menu to know more!")
  the_plugin = f"./{text}"
  if not os.path.exists(the_plugin):
      await plug.edit(f"No match found for `{text}`")
  
  await client.send_document(message.chat.id, f"./{text}", caption = f"Uploaded `{text}` successfully!!!", thumb = "logo.jpg")
  await asyncio.sleep(1)
  await plug.delete()
  
@friday_on_cmd(["font", "finst"],
    cmd_help={
    "help": "installs a font to the default directory",
    "example": "{ch}font or {ch}finst <reply to font file>"
    })

async def font_install(client, message):
    fontt = await edit_or_reply(message, "Processing...")

    if not message.reply_to_message:
       await fontt.edit("Reply To A ttf/otf/woff File To Install A Font")
       return

    if not message.reply_to_message.document:
        await fontt.edit("Is It A Even A Document?")
        return

    font_file_name = message.reply_to_message.document.file_name
    fext = font_file_name.split(".")[1]

    if os.path.exists(os.path.join("./bot_utils_files/Fonts/", font_file_name)):
        await fontt.edit("This Font is Already Installed!")
        return

    if not (fext.lower() == "ttf", "otf", "woff"):
        await fontt.edit("Only font files are allowed")
        return

    Escobar = await message.reply_to_message.download(file_name="./bot_utils_files/Fonts/")
    
    await fontt.edit(f"Sucessfully Installed **{font_file_name}**!")
	
@friday_on_cmd(["copy", "cp"],
    cmd_help={
    "help": "copies files from one directory to another",
    "example": "{ch}copy or {ch}cp /dir1/file1.ext | /dir2/"
    })

async def copy_files(client, message):
    copier = await edit_or_reply(message, "Processing...")
    text = get_text(message)

    if not text:
        await copier.edit("Please give me a valid input checkout help menu to know more!")
        return

    if " | " not in text:
        await copier.edit(f"Please use following formatting : `.copy or .cp /dir1/file1.ext | /dir2/`. **NOTE : Formatting shall be exactly how it's defined here!!!**")
        return

    if " | " in text:
        directories = text.split(" | ")
        dir1 = directories[0]
        dir2 = directories[1]

        if len(directories) < 2:
            await copier.edit("Please, give 2 arguments.")
            return

        if len(directories) > 2:
            await copier.edit("Please, only give 2 arguments.")
            return

        if len(directories) == 2:

            if not os.path.exists(f"/{dir1}"):
                await copier.edit(f"No match found for `{dir1}`")
                return

            else:

                dr1 = str(dir1).split("/")
                z     = dr1[len(dr1)-1]
                dst = f"{dir2}{z}"

                try:
                    sht.copyfile(f"{dir1}", f"{dst}")
                    await copier.edit(f"File copied from `{dir1}` to `{dst}` successfully.")

                except sht.SameFileError:
                    await copier.edit("Source and destination represents the same file.")

                except PermissionError:
                    await copier.edit("Permission denied.")

                except IsADirectoryError:
                        await copier.edit("Destination is a directory.")

        else:
            await copier.edit("An unknown error has occured!!! Please, report in @FridayChat. \n **Type code : `Else all`**")
            return

@friday_on_cmd(["move", "mv"],
    cmd_help={
    "help": "copies files from one directory to another",
    "example": "{ch}move or {ch}mv /dir1/file1.ext | /dir2/"
    })

async def move_files(client, message):
    mover = await edit_or_reply(message, "Processing...")
    text = get_text(message)

    if not text:
        await mover.edit("Please give me a valid input checkout help menu to know more!")
        return

    if " | " not in text:
        await mover.edit(f"Please use following formatting : `.move or .mv /dir1/file1.ext | /dir2/`. **NOTE : Formatting shall be exactly how it's defined here!!!**")
        return

    if " | " in text:
        directories = text.split(" | ")
        dir1 = directories[0]
        dir2 = directories[1]

        if len(directories) < 2:
            await mover.edit("Please, give 2 arguments.")
            return

        if len(directories) > 2:
            await mover.edit("Please, only give 2 arguments.")
            return

        if len(directories) == 2:

            if not os.path.exists(f"/{dir1}"):
                await mover.edit(f"No match found for `{dir1}`")
                return

            else:

                dr1 = str(dir1).split("/")
                z     = dr1[len(dr1)-1]
                dst = f"{dir2}{z}"

                try:
                    sht.copyfile(f"{dir1}", f"{dst}")
                    await mover.edit(f"File moved from `{dir1}` to `{dst}` successfully.")
                    os.remove(f"{dir1}")

                except sht.SameFileError:
                    await mover.edit("Source and destination represents the same file.")

                except PermissionError:
                    await mover.edit("Permission denied.")

                except IsADirectoryError:
                        await mover.edit("Destination is a directory.")

        else:
            await mover.edit("An unknown error has occured!!! Please, report in @FridayChat. \n **Type code : `Else all`**")
            return

@friday_on_cmd(["rnm"],
    cmd_help={
    "help": "Rename files in the directory",
    "example": "{ch}rnm /dir1/file1.ext | file2.ext"
    })

async def rename_files(client, message):
    renamer = await edit_or_reply(message, "Processing...")
    text = get_text(message)

    if not text:
        await renamer.edit("Please give me a valid input checkout help menu to know more!")
        return

    if " | " not in text:
        await renamer.edit(f"Please use following formatting : `.rnm /dir1/file1.ext | file2.ext`. **NOTE : Formatting shall be exactly how it's defined here!!!**")
        return

    if " | " in text:
        directories = text.split(" | ")
        dir1 = directories[0]
        dir2 = directories[1]

        if len(directories) < 2:
            await renamer.edit("Please, give 2 arguments.")
            return

        if len(directories) > 2:
            await renamer.edit("Please, only give 2 arguments.")
            return

        if len(directories) == 2:

            if not os.path.exists(f"/{dir1}"):
                await renamer.edit(f"No match found for `{dir1}`")
                return

            else:

                dr1 = str(dir1).rsplit("/", 1)
                z     = dr1[0]
                dst = f"{z}/{dir2}"

                try:
                    sht.copyfile(f"/{dir1}", f"/{dst}")
                    await renamer.edit(f"File renamed from `{dir1}` to `{dst}` successfully.")
                    os.remove(f"{dir1}")

                except sht.SameFileError:
                    await renamer.edit("Source and destination represents the same file.")

                except PermissionError:
                    await renamer.edit("Permission denied.")

                except IsADirectoryError:
                        await renamer.edit("Destination is a directory.")

        else:
            await renamer.edit("An unknown error has occured!!! Please, report in @FridayChat. \n **Type code : `Else all`**")
            return
