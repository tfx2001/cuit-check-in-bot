from bs4 import BeautifulSoup


def getFormValue(bs):
    result = {}

    # 获取输入框和hidden的值
    for inputElement in bs.findAll("input"):
        if inputElement.attrs["type"] in ["text", "hidden"]:
            result[inputElement.attrs["name"]] = (
                inputElement.attrs.get("value") != None
                and inputElement.attrs.get("value")
                or ""
            )

    # 获取select的值
    for selectElement in bs.findAll("select"):
        tName = selectElement.attrs["name"]
        tValue = None
        isFirstOption = True
        # 遍历选项
        for optionElement in selectElement.children:
            if optionElement.name == "option" and (
                optionElement.attrs.get("selected") != None or isFirstOption
            ):
                tValue = optionElement.attrs["value"]
                isFirstOption = False
        result[tName] = tValue

    # 获取textarea的值
    for textareaElement in bs.findAll("textarea"):
        result[textareaElement.attrs["name"]] = textareaElement.text

    result["B2"] = "提交打卡"

    return result
