from sklearn.metrics import accuracy_score, f1_score, recall_score
from utils import load_json


def evaluation(ground_truth_path: str, predictions_path: str) -> None:
    """
    计算以下评价指标
    准确率(Accuracy): 准确率是正确预测（无论是肯定还是否定）的数量与总预测数量的比例。
    召回率(Recall): 召回率是模型正确识别为reject的查询数与实际reject的查询总数的比例。
    F1分数(F1 Score): F1分数是准确率和召回率的调和平均数，是两者的平衡指标。
    """
    ground_truth_data = load_json(ground_truth_path)
    predictions_data = load_json(predictions_path)

    # 创建（id, query）到is_reject的映射
    ground_truth = {(item["query"]): item["is_reject"] for item in ground_truth_data}
    predictions = {(item["query"]): item["is_reject"] for item in predictions_data}

    # 对于ground_truth中的每个ID和query组合，获取预测结果，如果没有预测，则认为预测错误
    y_true = []
    y_pred = []
    for key, true_is_reject in ground_truth.items():
        if key in predictions:
            pred_is_reject = predictions[key]
            if not isinstance(pred_is_reject, bool):
                pred_is_reject = not true_is_reject
        else:
            # 如果predictions中没有该ID和query组合，设置预测结果为错误（即与真实结果相反）
            pred_is_reject = not true_is_reject
        y_true.append(true_is_reject)
        y_pred.append(pred_is_reject)

    # 计算评价指标
    accuracy = accuracy_score(y_true, y_pred)
    recall = recall_score(y_true, y_pred, pos_label=True)
    f1 = f1_score(y_true, y_pred, pos_label=True)
    right_num = [y_true[i] for i in range(len(y_true)) if y_true[i] == y_pred[i]]
    # 打印结果
    print("总条目数:", len(ground_truth), len(right_num))
    print("准确率: {:.2f}".format(accuracy))
    print("召回率: {:.2f}".format(recall))
    print("F1分数: {:.2f}".format(f1))
