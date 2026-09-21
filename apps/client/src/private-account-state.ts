import type { ApiSession, Bootstrap, ListRecord, Task } from './api';

export type PrivateAccountSnapshot = {
  inbox: Bootstrap['inbox'] | null;
  lists: ListRecord[];
  tasks: Task[];
  trash: Task[];
  taskDraft: string;
  listDraft: string;
  cachedPrivateResponses: ReadonlyMap<string, unknown>;
};

export function createPrivateAccountState(session: ApiSession) {
  let inbox: Bootstrap['inbox'] | null = null;
  let lists: ListRecord[] = [];
  let tasks: Task[] = [];
  let trash: Task[] = [];
  let taskDraft = '';
  let listDraft = '';
  const cachedPrivateResponses = new Map<string, unknown>();

  function clear() {
    inbox = null;
    lists = [];
    tasks = [];
    trash = [];
    taskDraft = '';
    listDraft = '';
    cachedPrivateResponses.clear();
  }

  const unregister = session.onPrivateStateClear(clear);

  return {
    hydrate(input: {
      inbox: Bootstrap['inbox'];
      lists: ListRecord[];
      tasks: Task[];
      trash?: Task[];
    }) {
      inbox = input.inbox;
      lists = [...input.lists];
      tasks = [...input.tasks];
      trash = [...(input.trash ?? [])];
    },
    setTaskDraft(value: string) {
      taskDraft = value;
    },
    setListDraft(value: string) {
      listDraft = value;
    },
    cachePrivateResponse(key: string, value: unknown) {
      cachedPrivateResponses.set(key, value);
    },
    snapshot(): PrivateAccountSnapshot {
      return {
        inbox,
        lists: [...lists],
        tasks: [...tasks],
        trash: [...trash],
        taskDraft,
        listDraft,
        cachedPrivateResponses: new Map(cachedPrivateResponses),
      };
    },
    clear,
    dispose() {
      unregister();
      clear();
    },
  };
}
