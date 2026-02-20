// BOUND: TARLAANALIZ_SSOT_v1_0_0.txt – canonical rules are referenced, not duplicated.
import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

export type MissionStatus = 'planned' | 'in_progress' | 'completed' | 'failed';

export interface MissionItem {
  id: string;
  name: string;
  status: MissionStatus;
  missionCode: string; // KR-016
}

const variantMap = {
  planned: 'info',
  in_progress: 'warning',
  completed: 'success',
  failed: 'danger'
} as const;

interface MissionListProps {
  missions: MissionItem[];
}

export function MissionList({ missions }: MissionListProps) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Görevler</CardTitle>
      </CardHeader>
      <CardContent>
        <ul className="space-y-2">
          {missions.map((mission) => (
            <li key={mission.id} className="flex items-center justify-between rounded-md border border-slate-200 p-3">
              <div>
                <p className="font-medium text-slate-900">{mission.name}</p>
                <p className="text-xs text-slate-500">{mission.missionCode}</p>
              </div>
              <Badge variant={variantMap[mission.status]}>{mission.status}</Badge>
            </li>
          ))}
        </ul>
      </CardContent>
    </Card>
  );
}
