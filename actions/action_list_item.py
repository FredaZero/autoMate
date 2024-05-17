
import uuid
from PyQt6.QtWidgets import QListWidgetItem
from PyQt6 import QtCore, QtWidgets
from actions.action_base import ActionBase
from actions.action_signal import ActionSignal
from actions.action_util import ActionUtil

class ActionListItem(QListWidgetItem):
    
   
    def __init__(self, action: ActionBase, widget_parent=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.action = action
        self.type = self.action.action_type
        self.setText(action.name)
        self._parent = widget_parent
        self.action_signal = ActionSignal()


    # 当父元素是包含类型的组件，减少当前元素的宽度让其能够被包含    
    def render(self):
        if self.type == "include":
            widget = QtWidgets.QWidget()
            widget.setStyleSheet("background-color: white;")
            label = QtWidgets.QLabel()
            label.setGeometry(QtCore.QRect(5, 10, 54, 12))
            label.setText("循环")
            layout = QtWidgets.QVBoxLayout()
            widget.setLayout(layout)
            layout.addWidget(label)
            widget.setFixedHeight(60)
            widget.setFixedWidth(self.get_parent().width() - 10)
            from actions.action_list import ActionList
            if not isinstance(self.data(QtCore.Qt.ItemDataRole.UserRole), ActionList):
                action_list = ActionList.load(self.action.args.action_list, self.get_parent(), self.get_parent().level + 1)
                action_list.action_signal.size_changed.connect(self._adjust_ui)
                action_list.action_signal.cancel_selection_to_father.connect(lambda : self.get_parent().clear_selection("father"))
                self.setData(QtCore.Qt.ItemDataRole.UserRole, action_list)
            else:
                action_list = self.data(QtCore.Qt.ItemDataRole.UserRole)
            action_list.setGeometry(QtCore.QRect(20, 30, widget.width() - 20, 20))
            layout.addWidget(action_list)
            self.setSizeHint(widget.size())
            self.get_parent().setItemWidget(self, widget)
            

    # 根据子元素数量调整当前元素尺寸大小
    def _adjust_ui(self):
        action_list = self.data(QtCore.Qt.ItemDataRole.UserRole)
        total_height = 0
        for item in action_list.get_action_list_items(action_list):
            total_height += action_list.visualItemRect(item).height()
        # 调整item大小
        self.setSizeHint(QtCore.QSize(action_list.width(), total_height + 60))
        self.get_widget().setFixedHeight(total_height + 60)
        # 发送元素大小更新的信号给父元素
        self.action_signal.size_changed_emit()
    
    def ActionListItem(self, parent):
        self._parent = parent

    def set_parent(self, parent):
        self._parent = parent

    def get_parent(self):
        return self._parent

    @staticmethod
    def load(data: dict):
        if data.get("name"):
            action_model = ActionUtil.get_action_by_name(data.get("name"))
            assert isinstance(action_model, ActionBase.__class__)
            action = action_model.model_validate(data.get("data"))
            action_item = ActionListItem(action)
            action.set_parent(action_item)
            return action_item
        else:
            raise ValueError("data must have a key named 'name'")

    def dump(self):
        return {"name": self.action.name, "data": self.action.model_dump()}
    
    def get_widget(self):
        return self.get_parent().itemWidget(self)